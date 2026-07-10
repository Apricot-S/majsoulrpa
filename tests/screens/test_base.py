import asyncio
import logging
from collections.abc import Mapping
from dataclasses import dataclass
from random import Random
from typing import Any, override

import pytest

import majsoulrpa.screens.base as screens_base
from majsoulrpa import RPAApp
from majsoulrpa.client.runtime import RPARuntime, ScreenshotScreenDetector
from majsoulrpa.config import AppConfig
from majsoulrpa.presentation import Region
from majsoulrpa.screens import Screen, ScreenContext, ScreenDetectionSpec
from majsoulrpa.screens.base import TemplateMatchResult
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenDetectionTimeoutError,
    ScreenStaleError,
)
from majsoulrpa.types import Callback


class LoginScreen(Screen):
    spec = ScreenDetectionSpec()

    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return cls.spec


class BrowserControllerSpy:
    def __init__(self) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.moved_points: list[tuple[float, float]] = []
        self.visited_urls: list[str] = []
        self.input_texts: list[str] = []
        self.pressed_keys: list[str] = []
        self.events: list[str] = []
        self.reloads = 0
        self.browser_host_stops = 0
        self.screenshot_bytes = b"\x89PNG\r\n\x1a\n"

    async def click(self, x: float, y: float) -> None:
        self.clicked_points.append((x, y))
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


@dataclass(frozen=True)
class TemplateMatchResultSpy:
    region: Region


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

    detector = ScreenshotScreenDetector(screenshot)

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

    context = ScreenContext(browser=BrowserControllerSpy())
    detector = ScreenshotScreenDetector(screenshot, context=context)

    screen = asyncio.run(detector.detect((FakeLoginScreen,)))

    assert isinstance(screen, FakeLoginScreen)
    assert screen.context is context


def test_screen_context_is_required_before_screen_operation() -> None:
    screen = LoginScreen()

    with pytest.raises(RuntimeError, match="ScreenContext"):
        _ = screen.context


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
            ScreenshotScreenDetector(screenshot),
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
            ScreenshotScreenDetector(screenshot),
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
            ScreenshotScreenDetector(screenshot),
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
        await screen.reload()
        await screen.goto_log("synthetic-log-id")
        await screen.stop_browser_host()
        await screen.stop_rpa()

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(call_apis())

    messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert messages == [
        "screen API called: screen=LoginScreen api=screenshot",
        "screen API called: screen=LoginScreen api=reload",
        "screen API called: screen=LoginScreen api=goto_log",
        "screen API called: screen=LoginScreen api=stop_browser_host",
        "screen API called: screen=LoginScreen api=stop_rpa",
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


def test_screen_can_go_to_log_url() -> None:
    browser = BrowserControllerSpy()
    screen = LoginScreen(context=ScreenContext(browser=browser))

    asyncio.run(screen.goto_log("synthetic-log-id"))

    assert browser.visited_urls == [
        "https://game.mahjongsoul.com/?paipu=synthetic-log-id",
    ]
    assert browser.events == ["goto_url"]


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
            ScreenshotScreenDetector(screenshot),
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
