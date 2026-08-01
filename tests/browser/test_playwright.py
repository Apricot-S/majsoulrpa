import asyncio
import base64
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Self, override

import pytest

import majsoulrpa.browser.playwright as browser_playwright
from majsoulrpa.browser.messages import (
    BrowserErrorResponse,
    ClickAndWaitForYostarAuthCommand,
    ClickCommand,
    ClickResponse,
    GotoUrlCommand,
    GotoUrlResponse,
    MoveMouseCommand,
    MoveMouseResponse,
    PressKeyCommand,
    PressKeyResponse,
    ReloadCommand,
    ReloadResponse,
    ScreenshotCommand,
    ScreenshotResponse,
    StopBrowserHostCommand,
    StopBrowserHostResponse,
    TextInputCommand,
    TextInputResponse,
    YostarAuthAcceptedResponse,
    YostarAuthRejectedResponse,
)
from majsoulrpa.browser.playwright import (
    CANVAS_SELECTOR,
    MAJSOUL_URL,
    PlaywrightBrowserBackend,
    PlaywrightCommandExecutor,
)
from majsoulrpa.config import AppConfig, BrowserConfig


class MouseSpy:
    def __init__(self, events: list[str] | None = None) -> None:
        self.clicks: list[tuple[float, float, float]] = []
        self.moves: list[tuple[float, float]] = []
        self.downs = 0
        self.ups = 0
        self._events = events

    async def click(self, x: float, y: float, *, delay: float) -> None:
        self.clicks.append((x, y, delay))
        if self._events is not None:
            self._events.append("click")

    async def move(self, x: float, y: float) -> None:
        self.moves.append((x, y))
        if self._events is not None:
            self._events.append("move")

    async def down(self) -> None:
        self.downs += 1
        if self._events is not None:
            self._events.append("down")

    async def up(self) -> None:
        self.ups += 1
        if self._events is not None:
            self._events.append("up")


class KeyboardSpy:
    def __init__(self) -> None:
        self.typed: list[tuple[str, float]] = []
        self.pressed: list[tuple[str, float]] = []

    async def type(self, text: str, *, delay: float) -> None:
        self.typed.append((text, delay))

    async def press(self, key: str, *, delay: float) -> None:
        self.pressed.append((key, delay))


class HttpRequestSpy:
    def __init__(self, method: str) -> None:
        self._method = method

    @property
    def method(self) -> str:
        return self._method


class HttpResponseSpy:
    def __init__(self, *, status: int, payload: object) -> None:
        self._url = browser_playwright.YOSTAR_AUTH_URL
        self._request = HttpRequestSpy("POST")
        self._status = status
        self._payload = payload

    @property
    def url(self) -> str:
        return self._url

    @property
    def request(self) -> browser_playwright.HttpRequestLike:
        return self._request

    @property
    def status(self) -> int:
        return self._status

    async def json(self) -> object:
        return self._payload


class ResponseValueSpy:
    def __init__(self, response: HttpResponseSpy) -> None:
        self._response = response

    def __await__(self):  # noqa: ANN204
        async def get_response() -> HttpResponseSpy:
            return self._response

        return get_response().__await__()


class ResponseInfoSpy:
    def __init__(self, response: HttpResponseSpy) -> None:
        self.value: Awaitable[browser_playwright.HttpResponseLike] = (
            ResponseValueSpy(response)
        )


class ResponseExpectationSpy:
    def __init__(
        self,
        events: list[str],
        predicate: Callable[[browser_playwright.HttpResponseLike], bool],
        response: HttpResponseSpy,
    ) -> None:
        self._events = events
        self._predicate = predicate
        self._response = response

    async def __aenter__(self) -> browser_playwright.ResponseInfoLike:
        self._events.append("expect_response")
        assert self._predicate(self._response)
        return ResponseInfoSpy(self._response)

    async def __aexit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        _ = (exc_type, exc_value, traceback)


class PageSpy:
    def __init__(self) -> None:
        self.events: list[str] = []
        self.mouse_spy = MouseSpy(self.events)
        self.keyboard_spy = KeyboardSpy()
        self.mouse: browser_playwright.MouseLike = self.mouse_spy
        self.keyboard: browser_playwright.KeyboardLike = self.keyboard_spy
        self.screenshot_types: list[str] = []
        self.screenshot_bytes = b"\x89PNG\r\n\x1a\n"
        self.visited_urls: list[str] = []
        self.reloads = 0
        self.waited_selectors: list[tuple[str, float]] = []
        self.evaluated_expressions: list[str] = []
        self.user_agent = "Mozilla/5.0 HeadlessChrome/120.0.0.0 Safari/537.36"
        self.yostar_response = HttpResponseSpy(
            status=200,
            payload={"Code": 200, "Data": {"Token": "synthetic-token"}},
        )

    async def goto(self, url: str) -> None:
        self.visited_urls.append(url)

    async def reload(self) -> None:
        self.reloads += 1

    async def evaluate(self, expression: str) -> str:
        self.evaluated_expressions.append(expression)
        return self.user_agent

    async def screenshot(self, **kwargs: str) -> bytes:
        self.screenshot_types.append(kwargs["type"])
        return self.screenshot_bytes

    async def wait_for_selector(
        self,
        selector: str,
        **kwargs: float,
    ) -> None:
        timeout = kwargs["timeout"]
        self.waited_selectors.append((selector, timeout))

    def expect_response(
        self,
        predicate: Callable[[browser_playwright.HttpResponseLike], bool],
        *,
        timeout: float,
    ) -> browser_playwright.ResponseExpectationLike:
        self.events.append(f"expect_response_timeout:{timeout}")
        return ResponseExpectationSpy(
            self.events,
            predicate,
            self.yostar_response,
        )


def test_playwright_command_executor_hovers_before_mouse_down(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    async def sleep(seconds: float) -> None:
        page.events.append(f"sleep:{seconds}")

    monkeypatch.setattr(browser_playwright.asyncio, "sleep", sleep)

    response = asyncio.run(
        executor.execute(
            ClickCommand(
                x=25,
                y=40,
                hover_delay_seconds=0.125,
                mouse_down_up_delay_seconds=0.1,
            ),
        ),
    )

    assert response == ClickResponse(x=25, y=40)
    assert page.events == [
        "move",
        "sleep:0.125",
        "down",
        "sleep:0.1",
        "up",
    ]
    assert page.mouse_spy.clicks == []


def test_playwright_command_executor_warp_clicks_with_mouse_delay() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            ClickCommand(
                x=25,
                y=40,
                hover_delay_seconds=None,
                mouse_down_up_delay_seconds=0.1,
            ),
        ),
    )

    assert response == ClickResponse(x=25, y=40)
    assert page.events == ["click"]
    assert page.mouse_spy.clicks == [(25, 40, 100)]


def test_playwright_command_executor_releases_mouse_when_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)
    sleep_count = 0

    async def sleep(seconds: float) -> None:
        nonlocal sleep_count
        sleep_count += 1
        page.events.append(f"sleep:{seconds}")
        if sleep_count == 2:
            raise asyncio.CancelledError

    monkeypatch.setattr(browser_playwright.asyncio, "sleep", sleep)

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(
            executor.execute(
                ClickCommand(
                    x=25,
                    y=40,
                    hover_delay_seconds=0.125,
                    mouse_down_up_delay_seconds=0.1,
                ),
            ),
        )

    assert page.events == [
        "move",
        "sleep:0.125",
        "down",
        "sleep:0.1",
        "up",
    ]


def test_playwright_executor_waits_for_yostar_auth_before_click() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            ClickAndWaitForYostarAuthCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
                timeout_seconds=15,
            ),
        ),
    )

    assert response == YostarAuthAcceptedResponse()
    assert page.events == [
        "expect_response_timeout:15000.0",
        "expect_response",
        "click",
    ]


def test_playwright_command_executor_returns_yostar_auth_rejection() -> None:
    page = PageSpy()
    page.yostar_response = HttpResponseSpy(
        status=200,
        payload={"Code": 100303, "Data": {}},
    )
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            ClickAndWaitForYostarAuthCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
                timeout_seconds=15,
            ),
        ),
    )

    assert response == YostarAuthRejectedResponse(application_code=100303)


@pytest.mark.parametrize(
    ("status", "payload", "expected_message"),
    [
        (
            500,
            {"Code": 200, "Data": {"Token": "synthetic-token"}},
            "Yostar authentication returned an unexpected HTTP status.",
        ),
        (
            200,
            {"Code": 200, "Data": {}},
            "Yostar authentication success response does not contain a token.",
        ),
    ],
)
def test_playwright_command_executor_returns_error_for_invalid_yostar_auth(
    status: int,
    payload: object,
    expected_message: str,
) -> None:
    page = PageSpy()
    page.yostar_response = HttpResponseSpy(status=status, payload=payload)
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            ClickAndWaitForYostarAuthCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
                timeout_seconds=15,
            ),
        ),
    )

    assert response == BrowserErrorResponse(message=expected_message)


def test_playwright_command_executor_moves_mouse() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            MoveMouseCommand(
                x=25,
                y=40,
            ),
        ),
    )

    assert response == MoveMouseResponse(x=25, y=40)
    assert page.mouse_spy.moves == [(25, 40)]


def test_playwright_command_executor_goes_to_url() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            GotoUrlCommand(url="https://example.invalid/path"),
        ),
    )

    assert response == GotoUrlResponse(url="https://example.invalid/path")
    assert page.visited_urls == ["https://example.invalid/path"]


def test_playwright_command_executor_reloads_page() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(executor.execute(ReloadCommand()))

    assert response == ReloadResponse()
    assert page.reloads == 1


def test_playwright_command_executor_accepts_stop_browser_host() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(executor.execute(StopBrowserHostCommand()))

    assert response == StopBrowserHostResponse()


def test_playwright_command_executor_types_with_millisecond_delay() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            TextInputCommand(
                text="player@example.invalid",
                character_delay_seconds=0.05,
            ),
        ),
    )

    assert response == TextInputResponse(text="player@example.invalid")
    assert page.keyboard_spy.typed == [("player@example.invalid", 50)]


def test_playwright_command_executor_presses_key() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            PressKeyCommand(
                key="Control+A",
                key_down_up_delay_seconds=0.05,
            ),
        ),
    )

    assert response == PressKeyResponse(key="Control+A")
    assert page.keyboard_spy.pressed == [("Control+A", 50)]


def test_playwright_command_executor_returns_base64_screenshot() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(executor.execute(ScreenshotCommand()))

    assert response == ScreenshotResponse(
        screenshot_base64=base64.b64encode(page.screenshot_bytes).decode(
            "ascii",
        ),
    )
    assert page.screenshot_types == ["png"]


def test_playwright_command_executor_returns_error_response() -> None:
    class BrokenMouse(MouseSpy):
        @override
        async def click(self, x: float, y: float, *, delay: float) -> None:
            _ = (x, y, delay)
            msg = "mouse failed"
            raise RuntimeError(msg)

    page = PageSpy()
    page.mouse = BrokenMouse()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            ClickCommand(
                x=25,
                y=40,
                hover_delay_seconds=None,
                mouse_down_up_delay_seconds=0.1,
            ),
        ),
    )

    assert response == BrowserErrorResponse(message="mouse failed")


class FakePage(PageSpy):
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        _ = (exc_type, exc_value, traceback)


class FakeContext:
    def __init__(self) -> None:
        self.pages: list[FakePage] = []
        self.new_page_called = 0
        self.closed = 0

    async def new_page(self) -> FakePage:
        self.new_page_called += 1
        page = FakePage()
        self.pages.append(page)
        return page

    async def close(self) -> None:
        self.closed += 1

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        _ = (exc_type, exc_value, traceback)
        await self.close()


class FakeBrowser:
    def __init__(self) -> None:
        self.context = FakeContext()
        self.new_context_kwargs: dict[str, object] | None = None
        self.closed = 0
        self.close_error: BaseException | None = None

    async def new_context(self, **kwargs: object) -> FakeContext:
        self.new_context_kwargs = kwargs
        return self.context

    async def close(self) -> None:
        self.closed += 1
        if self.close_error is not None:
            raise self.close_error

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        _ = (exc_type, exc_value, traceback)
        await self.close()


class FakeChromium:
    def __init__(self) -> None:
        self.browser = FakeBrowser()
        self.launched_browsers: list[FakeBrowser] = []
        self.persistent_context = FakeContext()
        self.launch_kwargs: dict[str, object] | None = None
        self.persistent_args: tuple[str, ...] | None = None
        self.persistent_kwargs: dict[str, object] | None = None

    async def launch(self, **kwargs: object) -> FakeBrowser:
        self.launch_kwargs = kwargs
        browser = FakeBrowser()
        self.launched_browsers.append(browser)
        return browser

    async def launch_persistent_context(
        self,
        *args: str,
        **kwargs: object,
    ) -> FakeContext:
        self.persistent_args = args
        self.persistent_kwargs = kwargs
        return self.persistent_context


class FakePlaywright:
    def __init__(self) -> None:
        self.chromium = FakeChromium()
        self.stopped = 0

    async def stop(self) -> None:
        self.stopped += 1


class FakePlaywrightStarter:
    def __init__(self, playwright: FakePlaywright) -> None:
        self._playwright = playwright
        self.started = 0

    async def start(self) -> FakePlaywright:
        self.started += 1
        return self._playwright


def test_playwright_browser_backend_starts_ephemeral_browser(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    playwright = FakePlaywright()
    starter = FakePlaywrightStarter(playwright)
    monkeypatch.setattr(
        browser_playwright,
        "async_playwright",
        lambda: starter,
    )
    backend = PlaywrightBrowserBackend()

    asyncio.run(backend.start(AppConfig()))

    assert starter.started == 1
    assert playwright.chromium.launch_kwargs == {
        "headless": False,
        "args": [
            "--window-position=0,0",
        ],
        "ignore_default_args": ["--mute-audio"],
    }
    [browser] = playwright.chromium.launched_browsers
    assert browser.new_context_kwargs == {
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": None,
    }
    assert isinstance(backend.page, FakePage)
    assert backend.page.visited_urls == [MAJSOUL_URL]
    assert backend.page.waited_selectors == [
        (CANVAS_SELECTOR, 60_000),
    ]

    asyncio.run(backend.stop())

    assert browser.context.closed == 1
    assert browser.closed == 1
    assert playwright.stopped == 1


def test_playwright_browser_backend_calls_page_ready_before_navigation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    playwright = FakePlaywright()
    starter = FakePlaywrightStarter(playwright)
    monkeypatch.setattr(
        browser_playwright,
        "async_playwright",
        lambda: starter,
    )
    backend = PlaywrightBrowserBackend()
    ready_pages: list[FakePage] = []

    async def page_ready(page: object) -> None:
        assert isinstance(page, FakePage)
        assert page.visited_urls == []
        ready_pages.append(page)

    asyncio.run(backend.start(AppConfig(), page_ready=page_ready))

    assert ready_pages == [backend.page]
    assert ready_pages[0].visited_urls == [MAJSOUL_URL]


def test_playwright_browser_backend_starts_persistent_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    playwright = FakePlaywright()
    starter = FakePlaywrightStarter(playwright)
    monkeypatch.setattr(
        browser_playwright,
        "async_playwright",
        lambda: starter,
    )
    backend = PlaywrightBrowserBackend()

    asyncio.run(
        backend.start(
            AppConfig(
                browser=BrowserConfig(
                    viewport_height=720,
                    headless=True,
                    user_data_dir=Path("user-data"),
                ),
            ),
        ),
    )

    assert playwright.chromium.persistent_args == ("user-data",)
    assert playwright.chromium.persistent_kwargs == {
        "headless": True,
        "viewport": {"width": 1280, "height": 720},
        "args": [
            "--window-position=0,0",
        ],
        "ignore_default_args": None,
        "user_agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
    }
    [user_agent_browser] = playwright.chromium.launched_browsers
    assert user_agent_browser.context.pages[0].visited_urls == []
    assert user_agent_browser.context.pages[0].evaluated_expressions == [
        "navigator.userAgent",
    ]
    assert user_agent_browser.context.closed == 1
    assert user_agent_browser.closed == 1
    assert isinstance(backend.page, FakePage)
    assert backend.page.visited_urls == [MAJSOUL_URL]
    assert backend.page.waited_selectors == [
        (CANVAS_SELECTOR, 60_000),
    ]

    asyncio.run(backend.stop())

    assert playwright.chromium.persistent_context.closed == 1
    assert playwright.chromium.browser.closed == 0
    assert playwright.stopped == 1


def test_playwright_browser_backend_stops_playwright_when_browser_close_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    playwright = FakePlaywright()
    starter = FakePlaywrightStarter(playwright)
    monkeypatch.setattr(
        browser_playwright,
        "async_playwright",
        lambda: starter,
    )
    backend = PlaywrightBrowserBackend()
    asyncio.run(backend.start(AppConfig()))
    [browser] = playwright.chromium.launched_browsers
    browser.close_error = RuntimeError("browser close failed")

    with pytest.raises(RuntimeError, match="browser close failed"):
        asyncio.run(backend.stop())

    assert browser.context.closed == 1
    assert browser.closed == 1
    assert playwright.stopped == 1


def test_playwright_browser_backend_keeps_cleaning_up_after_base_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    playwright = FakePlaywright()
    starter = FakePlaywrightStarter(playwright)
    monkeypatch.setattr(
        browser_playwright,
        "async_playwright",
        lambda: starter,
    )
    backend = PlaywrightBrowserBackend()
    asyncio.run(backend.start(AppConfig()))
    [browser] = playwright.chromium.launched_browsers
    browser.close_error = KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        asyncio.run(backend.stop())

    assert browser.context.closed == 1
    assert browser.closed == 1
    assert playwright.stopped == 1
