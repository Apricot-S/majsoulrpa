import asyncio
import base64
from collections.abc import Awaitable, Callable
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
from majsoulrpa.config import AppConfig
from majsoulrpa.viewport import viewport_width_for_height

MAJSOUL_URL = "https://game.mahjongsoul.com/"  # JP version
CANVAS_SELECTOR = "#unity-canvas"

_CANVAS_WAIT_TIMEOUT_SECONDS = 60

YOSTAR_AUTH_URL = "https://jp-sdk-api.yostarplat.com/yostar/get-auth"
HTTP_OK_STATUS = 200


class MouseLike(Protocol):
    async def click(self, x: float, y: float, *, delay: float) -> None: ...
    async def move(self, x: float, y: float) -> None: ...
    async def down(self) -> None: ...
    async def up(self) -> None: ...


class KeyboardLike(Protocol):
    async def press(self, key: str, *, delay: float) -> None: ...
    async def type(self, text: str, *, delay: float) -> None: ...


class HttpRequestLike(Protocol):
    @property
    def method(self) -> str: ...


class HttpResponseLike(Protocol):
    @property
    def url(self) -> str: ...

    @property
    def status(self) -> int: ...

    @property
    def request(self) -> HttpRequestLike: ...

    async def json(self) -> object: ...


class ResponseInfoLike(Protocol):
    value: Awaitable[HttpResponseLike]


class ResponseExpectationLike(Protocol):
    async def __aenter__(self) -> ResponseInfoLike: ...
    async def __aexit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None: ...


class PageLike(Protocol):
    mouse: MouseLike
    keyboard: KeyboardLike

    async def goto(self, url: str) -> object: ...
    async def reload(self) -> object: ...
    async def evaluate(self, expression: str) -> object: ...
    async def screenshot(self, **kwargs: str) -> bytes: ...
    async def wait_for_selector(
        self,
        selector: str,
        **kwargs: float,
    ) -> object: ...
    def expect_response(
        self,
        predicate: Callable[[HttpResponseLike], bool],
        *,
        timeout: float,
    ) -> ResponseExpectationLike: ...


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
                case GotoUrlCommand():
                    return await self._goto_url(command)
                case ReloadCommand():
                    return await self._reload()
                case StopBrowserHostCommand():
                    return StopBrowserHostResponse()
                case ClickAndWaitForYostarAuthCommand():
                    return await self._click_and_wait_for_yostar_auth(command)
        except Exception as error:  # noqa: BLE001
            return BrowserErrorResponse(message=str(error))

    async def _click(self, command: ClickCommand) -> ClickResponse:
        if command.hover_delay_seconds is None:
            await self._page.mouse.click(
                command.x,
                command.y,
                delay=command.mouse_down_up_delay_seconds * 1000,
            )
        else:
            await self._page.mouse.move(command.x, command.y)
            await asyncio.sleep(command.hover_delay_seconds)
            await self._page.mouse.down()
            try:
                await asyncio.sleep(command.mouse_down_up_delay_seconds)
            finally:
                await self._page.mouse.up()
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

    async def _goto_url(
        self,
        command: GotoUrlCommand,
    ) -> GotoUrlResponse:
        await self._page.goto(command.url)
        return GotoUrlResponse(url=command.url)

    async def _reload(self) -> ReloadResponse:
        await self._page.reload()
        return ReloadResponse()

    async def _click_and_wait_for_yostar_auth(
        self,
        command: ClickAndWaitForYostarAuthCommand,
    ) -> YostarAuthAcceptedResponse | YostarAuthRejectedResponse:
        async with self._page.expect_response(
            _is_yostar_auth_response,
            timeout=command.timeout_seconds * 1000,
        ) as response_info:
            await self._page.mouse.click(
                command.x,
                command.y,
                delay=command.mouse_down_up_delay_seconds * 1000,
            )

        response = await response_info.value
        if response.status != HTTP_OK_STATUS:
            msg = "Yostar authentication returned an unexpected HTTP status."
            raise TypeError(msg)

        try:
            payload = await response.json()
        except Exception as error:
            msg = "Yostar authentication returned invalid JSON."
            raise RuntimeError(msg) from error

        if not isinstance(payload, dict):
            msg = "Yostar authentication returned an unexpected JSON value."
            raise TypeError(msg)

        application_code = payload.get("Code")
        if isinstance(application_code, bool) or not isinstance(
            application_code,
            int,
        ):
            msg = (
                "Yostar authentication response does not contain a valid code."
            )
            raise TypeError(msg)
        if application_code != HTTP_OK_STATUS:
            return YostarAuthRejectedResponse(
                application_code=application_code,
            )

        data = payload.get("Data")
        if not isinstance(data, dict):
            msg = (
                "Yostar authentication success response does not contain data."
            )
            raise TypeError(msg)

        token = data.get("Token")
        if not isinstance(token, str) or not token:
            msg = (
                "Yostar authentication success response does not contain "
                "a token."
            )
            raise RuntimeError(msg)

        return YostarAuthAcceptedResponse()


def _is_yostar_auth_response(response: HttpResponseLike) -> bool:
    return (
        response.url == YOSTAR_AUTH_URL and response.request.method == "POST"
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

    async def start(
        self,
        config: AppConfig,
        *,
        page_ready: Callable[[object], Awaitable[None]] | None = None,
    ) -> None:
        self._playwright = await async_playwright().start()
        try:
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
            page = self._require_page()
            if page_ready is not None:
                await page_ready(page)
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
        page = self._require_page()
        await page.goto(MAJSOUL_URL)
        await page.wait_for_selector(
            CANVAS_SELECTOR,
            timeout=_CANVAS_WAIT_TIMEOUT_SECONDS * 1000,
        )

    def _require_page(self) -> Page:
        if self._page is None:
            msg = "Playwright page is not created."
            raise RuntimeError(msg)
        return self._page

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
        user_agent = await page.evaluate("navigator.userAgent")

    return str(user_agent).replace("HeadlessChrome", "Chrome")
