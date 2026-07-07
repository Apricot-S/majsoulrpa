import base64
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Protocol

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    ViewportSize,
    async_playwright,
)

from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserErrorResponse,
    BrowserResponse,
    ClickCommand,
    ClickResponse,
    MoveMouseCommand,
    MoveMouseResponse,
    PressKeyCommand,
    PressKeyResponse,
    ScreenshotCommand,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)
from majsoulrpa.config import AppConfig
from majsoulrpa.constants import (
    CANVAS_SELECTOR,
    CANVAS_WAIT_TIMEOUT_SECONDS,
    MAJSOUL_URL,
    USER_AGENT_PROBE_URL,
)
from majsoulrpa.viewport import viewport_width_for_height


class MouseLike(Protocol):
    async def click(self, x: float, y: float, *, delay: float) -> None: ...
    async def move(self, x: float, y: float) -> None: ...


class KeyboardLike(Protocol):
    async def press(self, key: str, *, delay: float) -> None: ...
    async def type(self, text: str, *, delay: float) -> None: ...


class PageLike(Protocol):
    mouse: MouseLike
    keyboard: KeyboardLike

    async def goto(self, url: str) -> object: ...
    async def evaluate(self, expression: str) -> object: ...
    async def screenshot(self, **kwargs: str) -> bytes: ...
    async def wait_for_selector(
        self,
        selector: str,
        **kwargs: float,
    ) -> object: ...


class PlaywrightCommandExecutor:
    def __init__(self, page: PageLike) -> None:
        self._page = page

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        try:
            match command:
                case ClickCommand():
                    return await self._click(command)
                case MoveMouseCommand():
                    return await self._move_mouse(command)
                case TextInputCommand():
                    return await self._input_text(command)
                case PressKeyCommand():
                    return await self._press_key(command)
                case ScreenshotCommand():
                    return await self._screenshot()
        except Exception as error:  # noqa: BLE001
            return BrowserErrorResponse(message=str(error))

    async def _click(self, command: ClickCommand) -> ClickResponse:
        await self._page.mouse.click(
            command.x,
            command.y,
            delay=command.mouse_down_up_delay_seconds * 1000,
        )
        return ClickResponse(x=command.x, y=command.y)

    async def _move_mouse(
        self,
        command: MoveMouseCommand,
    ) -> MoveMouseResponse:
        await self._page.mouse.move(command.x, command.y)
        return MoveMouseResponse(x=command.x, y=command.y)

    async def _input_text(
        self,
        command: TextInputCommand,
    ) -> TextInputResponse:
        await self._page.keyboard.type(
            command.text,
            delay=command.character_delay_seconds * 1000,
        )
        return TextInputResponse(text=command.text)

    async def _press_key(
        self,
        command: PressKeyCommand,
    ) -> PressKeyResponse:
        await self._page.keyboard.press(
            command.key,
            delay=command.key_down_up_delay_seconds * 1000,
        )
        return PressKeyResponse(key=command.key)

    async def _screenshot(self) -> ScreenshotResponse:
        screenshot = await self._page.screenshot(type="png")
        return ScreenshotResponse(
            screenshot_base64=base64.b64encode(screenshot).decode("ascii"),
        )


class PlaywrightBrowserBackend:
    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    @property
    def page(self) -> Page | None:
        return self._page

    async def start(self, config: AppConfig) -> None:
        self._playwright = await async_playwright().start()
        viewport_width = viewport_width_for_height(
            config.browser.viewport_height,
        )
        viewport = ViewportSize(
            width=viewport_width,
            height=config.browser.viewport_height,
        )
        args = [
            f"--window-position={config.browser.window_left},{config.browser.window_top}",
        ]
        ignore_default_args = (
            ["--mute-audio"] if not config.browser.headless else None
        )
        user_agent = (
            await _get_spoofed_user_agent(self._playwright)
            if config.browser.headless
            else None
        )

        try:
            if config.browser.user_data_dir is None:
                await self._start_ephemeral_browser(
                    headless=config.browser.headless,
                    viewport=viewport,
                    args=args,
                    ignore_default_args=ignore_default_args,
                    user_agent=user_agent,
                )
            else:
                await self._start_persistent_context(
                    user_data_dir=config.browser.user_data_dir,
                    headless=config.browser.headless,
                    viewport=viewport,
                    args=args,
                    ignore_default_args=ignore_default_args,
                    user_agent=user_agent,
                )
            await self._open_majsoul_page()
        except Exception:
            await self.stop()
            raise

    async def _start_ephemeral_browser(
        self,
        *,
        headless: bool,
        viewport: ViewportSize,
        args: list[str],
        ignore_default_args: list[str] | None,
        user_agent: str | None,
    ) -> None:
        if self._playwright is None:
            msg = "Playwright is not started."
            raise RuntimeError(msg)

        self._browser = await self._playwright.chromium.launch(
            headless=headless,
            args=args,
            ignore_default_args=ignore_default_args,
        )
        self._context = await self._browser.new_context(
            viewport=viewport,
            user_agent=user_agent,
        )
        self._page = await self._context.new_page()

    async def _start_persistent_context(
        self,
        *,
        user_data_dir: Path,
        headless: bool,
        viewport: ViewportSize,
        args: list[str],
        ignore_default_args: list[str] | None,
        user_agent: str | None,
    ) -> None:
        if self._playwright is None:
            msg = "Playwright is not started."
            raise RuntimeError(msg)

        self._context = await (
            self._playwright.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                viewport=viewport,
                args=args,
                ignore_default_args=ignore_default_args,
                user_agent=user_agent,
            )
        )
        self._page = (
            self._context.pages[0]
            if self._context.pages
            else await self._context.new_page()
        )

    async def _open_majsoul_page(self) -> None:
        if self._page is None:
            msg = "Playwright page is not created."
            raise RuntimeError(msg)

        await self._page.goto(MAJSOUL_URL)
        await self._page.wait_for_selector(
            CANVAS_SELECTOR,
            timeout=CANVAS_WAIT_TIMEOUT_SECONDS * 1000,
        )

    async def stop(self) -> None:
        context = self._context
        browser = self._browser
        playwright = self._playwright
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None

        async with AsyncExitStack() as stack:
            if playwright is not None:
                stack.push_async_callback(playwright.stop)
            if browser is not None:
                stack.push_async_callback(browser.close)
            if context is not None:
                stack.push_async_callback(context.close)


async def _get_spoofed_user_agent(playwright: Playwright) -> str:
    async with (
        await playwright.chromium.launch(headless=True) as browser,
        await browser.new_context() as context,
        await context.new_page() as page,
    ):
        await page.goto(USER_AGENT_PROBE_URL)
        user_agent = await page.evaluate("navigator.userAgent")

    return str(user_agent).replace("HeadlessChrome", "Chrome")
