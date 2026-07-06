import asyncio
import base64
from pathlib import Path
from typing import override

import pytest

import majsoulrpa.browser.playwright as browser_playwright
from majsoulrpa.browser import (
    BrowserErrorResponse,
    ClickCommand,
    ClickResponse,
    PlaywrightBrowserBackend,
    PlaywrightCommandExecutor,
    ScreenshotCommand,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)
from majsoulrpa.config import AppConfig, BrowserConfig


class MouseSpy:
    def __init__(self) -> None:
        self.clicks: list[tuple[float, float, float]] = []

    async def click(self, x: float, y: float, *, delay: float) -> None:
        self.clicks.append((x, y, delay))


class KeyboardSpy:
    def __init__(self) -> None:
        self.typed: list[tuple[str, float]] = []

    async def type(self, text: str, *, delay: float) -> None:
        self.typed.append((text, delay))


class PageSpy:
    def __init__(self) -> None:
        self.mouse_spy = MouseSpy()
        self.keyboard_spy = KeyboardSpy()
        self.mouse: browser_playwright.MouseLike = self.mouse_spy
        self.keyboard: browser_playwright.KeyboardLike = self.keyboard_spy
        self.screenshot_types: list[str] = []
        self.screenshot_bytes = b"\x89PNG\r\n\x1a\n"

    async def screenshot(self, **kwargs: str) -> bytes:
        self.screenshot_types.append(kwargs["type"])
        return self.screenshot_bytes


def test_playwright_command_executor_clicks_with_mouse_delay() -> None:
    page = PageSpy()
    executor = PlaywrightCommandExecutor(page)

    response = asyncio.run(
        executor.execute(
            ClickCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
            ),
        ),
    )

    assert response == ClickResponse(x=25, y=40)
    assert page.mouse_spy.clicks == [(25, 40, 100)]


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
                mouse_down_up_delay_seconds=0.1,
            ),
        ),
    )

    assert response == BrowserErrorResponse(message="mouse failed")


class FakePage(PageSpy):
    pass


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


class FakeBrowser:
    def __init__(self) -> None:
        self.context = FakeContext()
        self.new_context_kwargs: dict[str, object] | None = None
        self.closed = 0

    async def new_context(self, **kwargs: object) -> FakeContext:
        self.new_context_kwargs = kwargs
        return self.context

    async def close(self) -> None:
        self.closed += 1


class FakeChromium:
    def __init__(self) -> None:
        self.browser = FakeBrowser()
        self.persistent_context = FakeContext()
        self.launch_kwargs: dict[str, object] | None = None
        self.persistent_args: tuple[str, ...] | None = None
        self.persistent_kwargs: dict[str, object] | None = None

    async def launch(self, **kwargs: object) -> FakeBrowser:
        self.launch_kwargs = kwargs
        return self.browser

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
    assert playwright.chromium.browser.new_context_kwargs == {
        "viewport": {"width": 1920, "height": 1080},
    }
    assert isinstance(backend.page, FakePage)

    asyncio.run(backend.stop())

    assert playwright.chromium.browser.context.closed == 1
    assert playwright.chromium.browser.closed == 1
    assert playwright.stopped == 1


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
    }
    assert isinstance(backend.page, FakePage)

    asyncio.run(backend.stop())

    assert playwright.chromium.persistent_context.closed == 1
    assert playwright.chromium.browser.closed == 0
    assert playwright.stopped == 1
