import asyncio
import datetime
import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from random import Random
from typing import Any, override

import pytest

import majsoulrpa.screens.base as screens_base
from majsoulrpa import RPAApp
from majsoulrpa.client.runtime import RPARuntime, ScreenshotScreenDetector
from majsoulrpa.config import AppConfig
from majsoulrpa.presentation import Region
from majsoulrpa.screens import (
    Screen,
    ScreenDetectionSpec,
)
from majsoulrpa.screens import (
    ScreenContext as FrameworkScreenContext,
)
from majsoulrpa.screens.base import TemplateMatchResult
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenDetectionTimeoutError,
    ScreenInvalidArgumentError,
    ScreenStaleError,
)
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
    Direction,
    RawNotice,
    RawRequestResponse,
)
from majsoulrpa.sniffer.message_queue import (
    SnifferMessageQueue,
    SnifferMessageQueueOverflowError,
)
from majsoulrpa.types import Callback
from tests.sniffer.fakes import EMPTY_SNIFFER_MESSAGES


def ScreenContext(  # noqa: N802
    **kwargs: Any,  # noqa: ANN401
) -> FrameworkScreenContext:
    kwargs.setdefault("sniffer_messages", EMPTY_SNIFFER_MESSAGES)
    return FrameworkScreenContext(**kwargs)


class LoginScreen(Screen):
    spec = ScreenDetectionSpec()

    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return cls.spec

    async def get_sniffer_message(self) -> DecodedNotice:
        message = await self._get_sniffer_message()
        assert isinstance(message, DecodedNotice)
        return message

    def get_sniffer_message_nowait(self) -> DecodedNotice | None:
        message = self._get_sniffer_message_nowait()
        assert message is None or isinstance(message, DecodedNotice)
        return message

    def prepend_sniffer_message(self, message: DecodedNotice) -> None:
        self._prepend_sniffer_message(message)

    async def wait_for_sniffer_message(
        self,
        names: set[str],
        *,
        prepend_messages: bool = False,
    ) -> DecodedNotice:
        message = await self._wait_for_sniffer_message(
            names,
            prepend_messages=prepend_messages,
        )
        assert isinstance(message, DecodedNotice)
        return message


class BrowserControllerSpy:
    def __init__(self) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.click_warps: list[bool] = []
        self.moved_points: list[tuple[float, float]] = []
        self.visited_urls: list[str] = []
        self.input_texts: list[str] = []
        self.pressed_keys: list[str] = []
        self.events: list[str] = []
        self.reloads = 0
        self.browser_host_stops = 0
        self.screenshot_bytes = b"\x89PNG\r\n\x1a\n"

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        self.clicked_points.append((x, y))
        self.click_warps.append(warp)
        self.events.append("click")

    async def move_mouse(self, x: float, y: float) -> None:
        self.moved_points.append((x, y))
        self.events.append("move_mouse")

    async def goto_url(self, url: str) -> None:
        self.visited_urls.append(url)
        self.events.append("goto_url")

    async def reload(self) -> None:
        self.reloads += 1
        self.events.append("reload")

    async def stop_browser_host(self) -> None:
        self.browser_host_stops += 1
        self.events.append("stop_browser_host")

    async def click_and_wait_for_yostar_auth(
        self,
        x: float,
        y: float,
    ) -> object:
        await self.click(x, y)
        return object()

    async def input_text(self, text: str) -> None:
        self.input_texts.append(text)
        self.events.append("input_text")

    async def press_key(self, key: str) -> None:
        self.pressed_keys.append(key)
        self.events.append(f"press_key:{key}")

    async def screenshot(self) -> bytes:
        self.events.append("screenshot")
        return self.screenshot_bytes


class TemplateSpy:
    def __init__(self, *, matches: bool, region: Region | None = None) -> None:
        self.matches_result = matches
        self.region = region or Region(left=0, top=0, width=10, height=10)
        self.screenshots_for_find: list[object] = []
        self.screenshots_for_match: list[object] = []

    def match(self, screenshot: object) -> TemplateMatchResult:
        self.screenshots_for_match.append(screenshot)
        return TemplateMatchResultSpy(region=self.region)

    def find(self, screenshot: object) -> TemplateMatchResult | None:
        self.screenshots_for_find.append(screenshot)
        if not self.matches_result:
            return None
        return TemplateMatchResultSpy(region=self.region)

    def matches(self, screenshot: object) -> bool:
        return self.find(screenshot) is not None


class EventuallyMatchingTemplateSpy(TemplateSpy):
    def __init__(self, matching_screenshot: object) -> None:
        super().__init__(matches=False)
        self._matching_screenshot = matching_screenshot

    @override
    def find(self, screenshot: object) -> TemplateMatchResult | None:
        self.screenshots_for_find.append(screenshot)
        if screenshot != self._matching_screenshot:
            return None
        return TemplateMatchResultSpy(region=self.region)


@dataclass(frozen=True)
class TemplateMatchResultSpy:
    region: Region


class SnifferMessageSourceSpy:
    def __init__(self, *messages: DecodedSnifferMessage) -> None:
        self.messages = list(messages)
        self.prepend_messages: list[DecodedSnifferMessage] = []

    async def get(self) -> DecodedSnifferMessage:
        if not self.messages:
            future: asyncio.Future[DecodedSnifferMessage] = (
                asyncio.get_running_loop().create_future()
            )
            return await future
        return self.messages.pop(0)

    def get_nowait(self) -> DecodedSnifferMessage | None:
        if not self.messages:
            return None
        return self.messages.pop(0)

    def prepend(self, message: DecodedSnifferMessage) -> None:
        self.prepend_messages.insert(0, message)

    def prepend_many(self, messages: Sequence[DecodedSnifferMessage]) -> None:
        self.prepend_messages[0:0] = messages


def _notice(name: str) -> DecodedNotice:
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=name,
            payload=b"synthetic",
            observed_at=datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC),
        ),
        message={},
    )


def test_screen_formats_decoded_notice_without_raw_payload_bytes() -> None:
    message = DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=".lq.Test.notice",
            payload=b"raw-notice-payload",
            observed_at=datetime.datetime(
                2026,
                1,
                2,
                tzinfo=datetime.UTC,
            ),
        ),
        message={"nested": {"value": 1}},
    )

    formatted = screens_base._format_sniffer_message_for_log(message)

    assert formatted == (
        'Sniffer message: {"raw":{"direction":"inbound",'
        '"name":".lq.Test.notice",'
        '"observed_at":"2026-01-02T00:00:00+00:00"},'
        '"message":{"nested":{"value":1}}}'
    )
    assert "raw-notice-payload" not in formatted


def test_screen_formats_decoded_exchange_without_raw_payload_bytes() -> None:
    message = DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=".lq.Test.exchange",
            request=b"raw-request-payload",
            response=b"raw-response-payload",
            request_observed_at=datetime.datetime(
                2026,
                1,
                2,
                3,
                4,
                5,
                tzinfo=datetime.UTC,
            ),
            response_observed_at=datetime.datetime(
                2026,
                1,
                2,
                3,
                4,
                6,
                tzinfo=datetime.UTC,
            ),
        ),
        request={"requestValue": "synthetic"},
        response={"responseValue": 2},
    )

    formatted = screens_base._format_sniffer_message_for_log(message)

    assert formatted == (
        'Sniffer message: {"raw":{"request_direction":"outbound",'
        '"name":".lq.Test.exchange",'
        '"request_observed_at":"2026-01-02T03:04:05+00:00",'
        '"response_observed_at":"2026-01-02T03:04:06+00:00"},'
        '"request":{"requestValue":"synthetic"},'
        '"response":{"responseValue":2}}'
    )
    assert "raw-request-payload" not in formatted
    assert "raw-response-payload" not in formatted


def test_screen_exposes_detection_spec() -> None:
    assert LoginScreen.detection_spec() is LoginScreen.spec


def test_screen_requires_detection_spec() -> None:
    assert Screen.__abstractmethods__ == frozenset(
        {"before_callback", "detection_spec"},
    )


def test_screen_detector_detects_screen_from_fake_screenshot() -> None:
    login_screenshot = b"login"

    def matches_login(screenshot: object) -> bool:
        return screenshot == login_screenshot

    class FakeLoginScreen(Screen):
        @override
        async def before_callback(self) -> None:
            pass

        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=matches_login)

    async def screenshot() -> bytes:
        return login_screenshot

    detector = ScreenshotScreenDetector(
        screenshot,
        ScreenContext(browser=BrowserControllerSpy()),
    )

    screen = asyncio.run(detector.detect((FakeLoginScreen,)))

    assert isinstance(screen, FakeLoginScreen)


def test_screen_detector_injects_context_into_detected_screen() -> None:
    login_screenshot = b"login"

    def matches_login(screenshot: object) -> bool:
        return screenshot == login_screenshot

    class FakeLoginScreen(Screen):
        @override
        async def before_callback(self) -> None:
            pass

        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=matches_login)

    async def screenshot() -> bytes:
        return login_screenshot

    browser = BrowserControllerSpy()
    context = ScreenContext(browser=browser)
    detector = ScreenshotScreenDetector(screenshot, context=context)

    screen = asyncio.run(detector.detect((FakeLoginScreen,)))

    assert isinstance(screen, FakeLoginScreen)
    assert screen.context is context
    assert asyncio.run(screen.screenshot()) == browser.screenshot_bytes
    assert browser.events == ["screenshot"]


def test_screen_context_requires_sniffer_message_source() -> None:
    with pytest.raises(TypeError, match="sniffer_messages"):
        FrameworkScreenContext(  # ty: ignore[missing-argument]
            browser=BrowserControllerSpy(),
        )


def test_screen_context_exposes_current_account_id() -> None:
    class AccountStateStub:
        account_id: int | None = None

    account_state = AccountStateStub()
    context = ScreenContext(
        browser=BrowserControllerSpy(),
        account_state=account_state,
    )

    assert context.account_id is None

    account_state.account_id = 123456

    assert context.account_id == 123456


def test_screen_context_does_not_own_room_state() -> None:
    context = ScreenContext(browser=BrowserControllerSpy())

    assert not hasattr(context, "room_state_cache")


def test_screen_gets_and_puts_back_messages_through_context() -> None:
    first = _notice(".lq.First")
    second = _notice(".lq.Second")
    source = SnifferMessageSourceSpy(first, second)
    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
            sniffer_messages=source,
        ),
    )

    assert asyncio.run(screen.get_sniffer_message()) is first
    assert screen.get_sniffer_message_nowait() is second
    assert screen.get_sniffer_message_nowait() is None

    screen.prepend_sniffer_message(first)

    assert source.prepend_messages == [first]


def test_screen_waits_for_any_selected_message_and_discards_others() -> None:
    unrelated = _notice(".lq.Unrelated")
    expected = _notice(".lq.Second")
    source = SnifferMessageSourceSpy(unrelated, expected)
    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
            sniffer_messages=source,
        ),
    )

    actual = asyncio.run(
        screen.wait_for_sniffer_message({".lq.First", ".lq.Second"}),
    )

    assert actual is expected
    assert source.prepend_messages == []


def test_screen_can_prepend_all_read_messages_in_original_order() -> None:
    first = _notice(".lq.UnrelatedFirst")
    second = _notice(".lq.UnrelatedSecond")
    expected = _notice(".lq.Target")
    source = SnifferMessageSourceSpy(first, second, expected)
    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
            sniffer_messages=source,
        ),
    )

    actual = asyncio.run(
        screen.wait_for_sniffer_message(
            {".lq.Target"},
            prepend_messages=True,
        ),
    )

    assert actual is expected
    assert source.prepend_messages == [first, second, expected]


def test_screen_restores_prefix_before_existing_prepend_messages() -> None:
    first = _notice(".lq.First")
    second = _notice(".lq.Second")
    remaining = _notice(".lq.Remaining")
    new = _notice(".lq.New")
    source = SnifferMessageQueue(capacity=4, max_payload_bytes=1024)
    source.prepend_many([first, second, remaining])
    source.enqueue(new)
    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
            sniffer_messages=source,
        )
    )

    actual = asyncio.run(
        screen.wait_for_sniffer_message(
            {second.raw.name},
            prepend_messages=True,
        )
    )

    assert actual is second
    assert (
        asyncio.run(
            screen.wait_for_sniffer_message(
                {first.raw.name},
                prepend_messages=True,
            )
        )
        is first
    )
    assert [source.get_nowait() for _ in range(4)] == [
        first,
        second,
        remaining,
        new,
    ]


def test_screen_propagates_batch_restoration_overflow() -> None:
    first = _notice(".lq.First")
    remaining = _notice(".lq.Remaining")
    new = _notice(".lq.New")

    class ArrivingMessageQueue(SnifferMessageQueue):
        @override
        async def get(self) -> DecodedSnifferMessage:
            message = await super().get()
            self.enqueue(new)
            return message

    source = ArrivingMessageQueue(capacity=2, max_payload_bytes=1024)
    source.prepend_many([first, remaining])
    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
            sniffer_messages=source,
        )
    )

    with pytest.raises(SnifferMessageQueueOverflowError):
        asyncio.run(
            screen.wait_for_sniffer_message(
                {first.raw.name},
                prepend_messages=True,
            )
        )

    assert source.get_nowait() is remaining
    assert source.get_nowait() is new
    assert source.get_nowait() is None


def test_screen_restores_unmatched_messages_when_wait_is_cancelled() -> None:
    async def exercise() -> None:
        unrelated = _notice(".lq.Unrelated")
        source = SnifferMessageSourceSpy(unrelated)
        screen = LoginScreen(
            context=ScreenContext(
                browser=BrowserControllerSpy(),
                sniffer_messages=source,
            ),
        )
        task = asyncio.create_task(
            screen.wait_for_sniffer_message(
                {".lq.Target"},
                prepend_messages=True,
            ),
        )
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert source.prepend_messages == [unrelated]

    asyncio.run(exercise())


def test_screen_rejects_empty_sniffer_message_names() -> None:
    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
        ),
    )

    with pytest.raises(ValueError, match="must not be empty"):
        asyncio.run(screen.wait_for_sniffer_message(set()))


def test_screen_retries_screenshot_until_template_can_be_clicked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    class SequencedScreenshotBrowserSpy(BrowserControllerSpy):
        def __init__(self) -> None:
            super().__init__()
            self._screenshots = iter((b"first", b"second", b"matched"))

        @override
        async def screenshot(self) -> bytes:
            return next(self._screenshots)

    browser = SequencedScreenshotBrowserSpy()
    template = EventuallyMatchingTemplateSpy(b"matched")
    screen = LoginScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(screens_base.asyncio, "sleep", sleep)

    result = asyncio.run(screen.wait_and_click_template(template))

    assert result.region == template.region
    assert template.screenshots_for_find == [b"first", b"second", b"matched"]
    assert sleeps == [0.5, 0.5]
    assert len(browser.clicked_points) == 1


def test_screen_template_retry_timeout_is_controlled_by_caller() -> None:
    async def exercise() -> None:
        screen = LoginScreen(
            context=ScreenContext(browser=BrowserControllerSpy()),
        )
        async with asyncio.timeout(0.001):
            await screen.wait_and_click_template(TemplateSpy(matches=False))

    with pytest.raises(TimeoutError):
        asyncio.run(exercise())


def test_false_screen_detection_does_not_call_callback() -> None:
    fake_screenshot = b"\x89PNG\r\n\x1a\n"

    class NeverScreen(Screen):
        @override
        async def before_callback(self) -> None:
            pass

        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=lambda _screenshot: False)

    async def screenshot() -> bytes:
        return fake_screenshot

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        _ = config
        return RPARuntime(
            callbacks,
            ScreenshotScreenDetector(
                screenshot, ScreenContext(browser=BrowserControllerSpy())
            ),
            should_stop=lambda: True,
        )

    app = RPAApp(runtime_factory=runtime_factory)
    called = False

    @app.on(NeverScreen)
    async def handle_never(_screen: NeverScreen, data: object) -> object:
        nonlocal called
        called = True
        return data

    with pytest.raises(ScreenDetectionTimeoutError) as exc_info:
        asyncio.run(app.run(AppConfig(), object(), detection_timeout=0.001))

    assert exc_info.value.screenshot == fake_screenshot
    assert called is False


def test_screen_detection_exception_is_not_hidden() -> None:
    def raise_detection_error(_screenshot: object) -> bool:
        msg = "detection failed"
        raise RuntimeError(msg)

    class BrokenScreen(Screen):
        @override
        async def before_callback(self) -> None:
            pass

        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=raise_detection_error)

    async def screenshot() -> bytes:
        return b"broken"

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        _ = config
        return RPARuntime(
            callbacks,
            ScreenshotScreenDetector(
                screenshot, ScreenContext(browser=BrowserControllerSpy())
            ),
            should_stop=lambda: True,
        )

    app = RPAApp(runtime_factory=runtime_factory)

    @app.on(BrokenScreen)
    async def handle_broken(_screen: BrokenScreen, data: object) -> object:
        return data

    with pytest.raises(RuntimeError, match="detection failed"):
        asyncio.run(app.run(AppConfig(), object()))


def test_multiple_matching_screens_use_registration_order() -> None:
    matching_screenshot = b"match"
    missing_screenshot = b"miss"

    class FirstScreen(Screen):
        @override
        async def before_callback(self) -> None:
            pass

        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(
                predicate=lambda screenshot: screenshot == matching_screenshot,
            )

    class SecondScreen(Screen):
        @override
        async def before_callback(self) -> None:
            pass

        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(
                predicate=lambda screenshot: screenshot == matching_screenshot,
            )

    screenshots = [matching_screenshot, missing_screenshot]

    async def screenshot() -> bytes:
        if not screenshots:
            return missing_screenshot
        return screenshots.pop(0)

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        _ = config
        return RPARuntime(
            callbacks,
            ScreenshotScreenDetector(
                screenshot, ScreenContext(browser=BrowserControllerSpy())
            ),
            should_stop=lambda: True,
        )

    app = RPAApp(runtime_factory=runtime_factory)

    @app.on(FirstScreen)
    async def handle_first(_screen: FirstScreen, _data: object) -> str:
        return "first"

    @app.on(SecondScreen)
    async def handle_second(_screen: SecondScreen, _data: object) -> str:
        return "second"

    result = asyncio.run(app.run(AppConfig(), None, detection_timeout=0.001))

    assert result == "first"


def test_screen_fills_scaled_region(monkeypatch: pytest.MonkeyPatch) -> None:
    browser = BrowserControllerSpy()
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        browser.events.append("sleep")

    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )

    monkeypatch.setattr(screens_base.asyncio, "sleep", sleep)

    asyncio.run(
        screen.fill_region(
            Region(left=300, top=150, width=6, height=3),
            "player@example.invalid",
        ),
    )

    [(x, y)] = browser.clicked_points
    assert 200 < x < 204
    assert 100 < y < 102
    assert sleeps == [0.5]
    assert browser.events == ["click", "sleep", "input_text"]
    assert browser.input_texts == ["player@example.invalid"]


def test_screen_can_clear_region_before_filling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        browser.events.append("sleep")

    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
        ),
    )

    monkeypatch.setattr(screens_base.asyncio, "sleep", sleep)

    asyncio.run(
        screen.fill_region(
            Region(left=0, top=0, width=10, height=10),
            "player@example.invalid",
            clear=True,
        ),
    )

    assert browser.pressed_keys == ["ControlOrMeta+A", "Backspace"]
    assert sleeps == [0.5, 0.5, 0.5]
    assert browser.events == [
        "click",
        "sleep",
        "press_key:ControlOrMeta+A",
        "sleep",
        "press_key:Backspace",
        "sleep",
        "input_text",
    ]
    assert browser.input_texts == ["player@example.invalid"]


def test_screen_clicks_scaled_region(
    caplog: pytest.LogCaptureFixture,
) -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(
            screen.click_region(Region(left=300, top=150, width=6, height=3)),
        )

    [(x, y)] = browser.clicked_points
    assert 200 < x < 204
    assert 100 < y < 102
    assert browser.events == ["click"]
    assert not [
        record
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]


def test_screen_moves_to_scaled_region() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )

    asyncio.run(
        screen.move_region(Region(left=300, top=150, width=6, height=3)),
    )

    [(x, y)] = browser.moved_points
    assert 200 < x < 204
    assert 100 < y < 102
    assert browser.clicked_points == []
    assert browser.events == ["move_mouse"]


def test_screen_forwards_warp_region_click() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    asyncio.run(
        screen.click_region(
            Region(left=300, top=150, width=6, height=3),
            warp=True,
        ),
    )

    assert browser.click_warps == [True]


def test_screen_finds_template() -> None:
    browser = BrowserControllerSpy()
    browser.screenshot_bytes = b"match"
    template = TemplateSpy(matches=True)
    screen = LoginScreen(
        context=ScreenContext(browser=browser),
    )

    result = asyncio.run(screen.find_template(template))

    assert result == TemplateMatchResultSpy(
        region=Region(left=0, top=0, width=10, height=10),
    )
    assert browser.events == ["screenshot"]
    assert template.screenshots_for_find == [b"match"]


def test_screen_returns_none_when_template_is_missing() -> None:
    browser = BrowserControllerSpy()
    browser.screenshot_bytes = b"miss"
    template = TemplateSpy(matches=False)
    screen = LoginScreen(
        context=ScreenContext(browser=browser),
    )

    assert asyncio.run(screen.find_template(template)) is None
    assert browser.events == ["screenshot"]
    assert template.screenshots_for_find == [b"miss"]


def test_screen_clicks_required_template_without_scaling() -> None:
    browser = BrowserControllerSpy()
    browser.screenshot_bytes = b"match"
    template = TemplateSpy(
        matches=True,
        region=Region(left=300, top=150, width=6, height=3),
    )
    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )

    result = asyncio.run(
        screen.click_template(template, message="missing template"),
    )

    assert result.region == Region(left=300, top=150, width=6, height=3)
    assert browser.events == ["screenshot", "click"]
    assert template.screenshots_for_find == [b"match"]
    assert template.screenshots_for_match == []
    [(x, y)] = browser.clicked_points
    assert 300 < x < 306
    assert 150 < y < 153


def test_screen_forwards_warp_for_all_template_click_apis() -> None:
    browser = BrowserControllerSpy()
    browser.screenshot_bytes = b"match"
    template = TemplateSpy(matches=True)
    screen = LoginScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    asyncio.run(
        screen.click_template(
            template,
            message="missing template",
            warp=True,
        )
    )
    asyncio.run(screen.click_template_if_present(template, warp=True))
    asyncio.run(screen.wait_and_click_template(template, warp=True))

    assert browser.click_warps == [True, True, True]


def test_screen_raises_when_required_template_does_not_match() -> None:
    browser = BrowserControllerSpy()
    browser.screenshot_bytes = b"miss"
    template = TemplateSpy(matches=False)
    screen = LoginScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    with pytest.raises(
        ScreenDetectionError, match="missing template"
    ) as exc_info:
        asyncio.run(
            screen.click_template(template, message="missing template")
        )

    assert exc_info.value.screenshot == b"miss"
    assert browser.events == ["screenshot"]
    assert template.screenshots_for_find == [b"miss"]
    assert template.screenshots_for_match == []
    assert browser.clicked_points == []


def test_screen_does_not_click_if_optional_template_does_not_match() -> None:
    browser = BrowserControllerSpy()
    browser.screenshot_bytes = b"miss"
    template = TemplateSpy(matches=False)
    screen = LoginScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    result = asyncio.run(screen.click_template_if_present(template))

    assert result is False
    assert browser.events == ["screenshot"]
    assert template.screenshots_for_find == [b"miss"]
    assert template.screenshots_for_match == []
    assert browser.clicked_points == []


def test_screen_context_requests_stop() -> None:
    requested = False

    async def request_stop() -> None:
        nonlocal requested
        requested = True

    context = ScreenContext(
        browser=BrowserControllerSpy(),
        request_stop=request_stop,
    )

    asyncio.run(context.request_stop())

    assert requested is True


def test_screen_context_awaits_falsey_stop_requester() -> None:
    class StopRequesterSpy:
        def __init__(self) -> None:
            self.calls = 0

        def __bool__(self) -> bool:
            return False

        async def __call__(self) -> None:
            self.calls += 1

    requester = StopRequesterSpy()
    context = ScreenContext(
        browser=BrowserControllerSpy(), request_stop=requester
    )

    asyncio.run(context.request_stop())

    assert requester.calls == 1


def test_screen_context_default_stop_request_is_noop() -> None:
    browser = BrowserControllerSpy()
    context = ScreenContext(browser=browser)

    asyncio.run(context.request_stop())

    assert browser.events == []


@pytest.mark.parametrize(
    "error",
    [RuntimeError("synthetic stop failure"), asyncio.CancelledError()],
    ids=["failure", "cancellation"],
)
def test_screen_context_propagates_stop_request_error(
    error: BaseException,
) -> None:
    async def request_stop() -> None:
        raise error

    context = ScreenContext(
        browser=BrowserControllerSpy(), request_stop=request_stop
    )

    with pytest.raises(type(error)) as caught:
        asyncio.run(context.request_stop())

    assert caught.value is error


def test_screen_can_request_rpa_stop() -> None:
    requested = False

    async def request_stop() -> None:
        nonlocal requested
        requested = True

    screen = LoginScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(),
            request_stop=request_stop,
        ),
    )

    asyncio.run(screen.stop_rpa())

    assert requested is True


def test_screen_can_request_browser_host_stop() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    asyncio.run(screen.stop_browser_host())

    assert browser.browser_host_stops == 1
    assert browser.events == ["stop_browser_host"]


def test_screen_context_browser_can_take_screenshot() -> None:
    browser = BrowserControllerSpy()
    context = ScreenContext(browser=browser)

    screenshot = asyncio.run(context.browser.screenshot())

    assert screenshot == b"\x89PNG\r\n\x1a\n"
    assert browser.events == ["screenshot"]


def test_screen_can_take_screenshot() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    screenshot = asyncio.run(screen.screenshot())

    assert screenshot == b"\x89PNG\r\n\x1a\n"
    assert browser.events == ["screenshot"]


def test_screen_high_level_apis_log_outer_calls(
    caplog: pytest.LogCaptureFixture,
) -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    async def call_apis() -> None:
        await screen.screenshot()
        await screen.goto_log("synthetic-log-id")
        await screen.stop_browser_host()
        await screen.stop_rpa()
        await screen.reload()

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(call_apis())

    messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert messages == [
        "screen API called: screen=LoginScreen api=screenshot",
        "screen API called: screen=LoginScreen api=goto_log",
        "screen API called: screen=LoginScreen api=stop_browser_host",
        "screen API called: screen=LoginScreen api=stop_rpa",
        "screen API called: screen=LoginScreen api=reload",
    ]
    assert "synthetic-log-id" not in caplog.text


def test_stale_screen_rejects_public_api_with_screenshot(
    caplog: pytest.LogCaptureFixture,
) -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))
    screen._mark_stale()

    with (
        caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"),
        pytest.raises(
            ScreenStaleError,
            match="LoginScreen is stale",
        ) as exc_info,
    ):
        asyncio.run(screen.screenshot())

    assert exc_info.value.screenshot == browser.screenshot_bytes
    assert browser.events == ["screenshot"]
    assert "screen=LoginScreen api=screenshot" in caplog.text


def test_screen_can_reload_current_page() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    asyncio.run(screen.reload())

    assert browser.reloads == 1
    assert browser.events == ["reload"]


def test_screen_becomes_stale_after_reload() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    asyncio.run(screen.reload())

    with pytest.raises(ScreenStaleError, match="LoginScreen is stale"):
        asyncio.run(screen.screenshot())
    assert browser.events == ["reload", "screenshot"]


@pytest.mark.parametrize(
    "log_id",
    [
        "synthetic-log-id",
        "260101-00000000-0000-0000-0000-000000000000",
        "260101-00000000-0000-0000-0000-000000000000_a123456789",
        "abcdef-ghijklmn-opqr-stuv-wxyz-abcdefghijkl_a123456789_2",
        "X",
    ],
    ids=[
        "synthetic",
        "basic",
        "viewpoint",
        "obfuscated",
        "no-structure-check",
    ],
)
def test_screen_can_go_to_log_url(log_id: str) -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    asyncio.run(screen.goto_log(log_id))

    assert browser.visited_urls == [
        f"https://game.mahjongsoul.com/?paipu={log_id}",
    ]
    assert browser.events == ["goto_url"]


@pytest.mark.parametrize(
    "log_id",
    [
        "",
        "synthetic&other=value",
        "synthetic#fragment",
        "synthetic space",
        "synthetic+value",
        "synthetic%20value",
        "synthetic/part",
        "synthetic日本語",
    ],
    ids=[
        "empty",
        "query",
        "fragment",
        "space",
        "plus",
        "percent",
        "slash",
        "non-ascii",
    ],
)
def test_screen_rejects_invalid_log_id_without_navigation_or_disclosure(
    log_id: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    with (
        caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"),
        pytest.raises(ScreenInvalidArgumentError, match="Log ID") as caught,
    ):
        asyncio.run(screen.goto_log(log_id))

    assert browser.visited_urls == []
    assert caught.value.screenshot == browser.screenshot_bytes
    assert browser.events == ["screenshot"]
    if log_id:
        assert log_id not in str(caught.value)
        assert log_id not in repr(caught.value)
        assert log_id not in caplog.text


def test_runtime_calls_screen_before_callback() -> None:
    matching_screenshot = b"match"
    missing_screenshot = b"miss"

    events: list[str] = []

    class PreHookScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(
                predicate=lambda screenshot: screenshot == matching_screenshot,
            )

        @override
        async def before_callback(self) -> None:
            events.append("before_callback")

    screenshots = [matching_screenshot]

    async def screenshot() -> bytes:
        if screenshots:
            return screenshots.pop(0)
        return missing_screenshot

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        _ = config
        return RPARuntime(
            callbacks,
            ScreenshotScreenDetector(
                screenshot, ScreenContext(browser=BrowserControllerSpy())
            ),
            should_stop=lambda: True,
        )

    app = RPAApp(runtime_factory=runtime_factory)

    @app.on(PreHookScreen)
    async def handle_pre_hook(
        _screen: PreHookScreen,
        data: object,
    ) -> object:
        events.append("callback")
        return data

    data = object()
    result = asyncio.run(app.run(AppConfig(), data, detection_timeout=0.001))

    assert result is data
    assert events == ["before_callback", "callback"]
