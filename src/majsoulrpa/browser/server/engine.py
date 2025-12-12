import base64
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Never

from playwright.async_api import Page, ViewportSize, async_playwright

from majsoulrpa.browser import schemas
from majsoulrpa.browser.server import core
from majsoulrpa.browser.server.config import Config
from majsoulrpa.constants import DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.exceptions import UserInputError

MAJSOUL_URL = "https://game.mahjongsoul.com/"  # JP version
MAJSOUL_LOG_URL = "https://game.mahjongsoul.com/?paipu="  # JP version

PAGE_WAIT_TIMEOUT = 30_000

type BrowserEngineRunner = Callable[
    [Config, Option, core.ServerRunner],
    Coroutine[Any, Any, None],
]


@dataclass(frozen=True)
class Option:
    user_data_dir: Path | None
    window_left: int
    window_top: int
    viewport_height: int
    headless: bool
    url: str = MAJSOUL_URL

    def __post_init__(self) -> None:
        if self.user_data_dir is not None:
            resolved = resolve_user_data_dir(self.user_data_dir)
            object.__setattr__(self, "user_data_dir", resolved)

        validate_viewport_height(self.viewport_height)


def resolve_user_data_dir(path: Path) -> Path:
    p = path.resolve(strict=False)
    if p.exists() and p.is_file():
        msg = "invalid user-data-dir: file exists"
        raise UserInputError(msg)
    return p


def validate_viewport_height(h: int) -> None:
    if h <= 0:
        msg = f"viewport-height must be positive: {h}"
        raise UserInputError(msg)

    if h % 9 != 0:
        msg = f"viewport-height is not a valid 16:9 resolution: {h}"
        raise UserInputError(msg)

    w = h * 16 // 9
    if w * 9 != h * 16:
        msg = f"viewport-height is not a valid 16:9 resolution: {h}"
        raise UserInputError(msg)


def _create_browser_args(config: Config, option: Option) -> list[str]:
    window_position = (
        f"--window-position={option.window_left},{option.window_top}"
    )
    proxy_server = f"--proxy-server=http://localhost:{config.proxy_port}"
    ignore_certificate_errors = "--ignore-certificate-errors"
    return [window_position, proxy_server, ignore_certificate_errors]


def _create_ignored_default_args(option: Option) -> list[str]:
    return [] if option.headless else ["--mute-audio"]


def _get_viewport_size(option: Option) -> ViewportSize:
    height = option.viewport_height
    width = height * 16 // 9
    return ViewportSize(width=width, height=height)


def _get_scale(viewport: ViewportSize) -> float:
    return viewport["height"] / DEFAULT_VIEWPORT_HEIGHT


async def _handle_resolution(
    viewport: ViewportSize,
    scale: float,
) -> schemas.ResolutionResponse:
    return schemas.ResolutionResponse(
        width=viewport["width"],
        height=viewport["height"],
        scale=scale,
    )


async def _handle_move_mouse(
    page: Page,
    req: schemas.MoveMouseRequest,
) -> schemas.MoveMouseResponse:
    x = req.x
    y = req.y
    await page.mouse.move(x=x, y=y)
    return schemas.MoveMouseResponse(x=x, y=y)


async def _handle_click_mouse(
    page: Page,
    req: schemas.ClickMouseRequest,
) -> schemas.ClickMouseResponse:
    x = req.x
    y = req.y
    delay = req.delay
    await page.mouse.click(x=x, y=y, delay=delay)
    return schemas.ClickMouseResponse(x=x, y=y, delay=delay)


async def _handle_press_key(
    page: Page,
    req: schemas.PressKeyRequest,
) -> schemas.PressKeyResponse:
    key = req.key
    delay = req.delay
    await page.keyboard.press(key=key, delay=delay)
    return schemas.PressKeyResponse(key=key, delay=delay)


async def _handle_type_key(
    page: Page,
    req: schemas.TypeKeyRequest,
) -> schemas.TypeKeyResponse:
    text = req.text
    delay = req.delay
    await page.keyboard.type(text=text, delay=delay)
    return schemas.TypeKeyResponse(text=text, delay=delay)


async def _handle_screenshot(page: Page) -> schemas.ScreenshotResponse:
    image = await page.screenshot()
    image_b64 = base64.b64encode(image).decode(encoding="utf-8")
    return schemas.ScreenshotResponse(image=image_b64)


async def _handle_log(
    page: Page,
    req: schemas.LogRequest,
) -> schemas.LogResponse:
    await page.goto(f"{MAJSOUL_LOG_URL}{req.log_id}")
    return schemas.LogResponse()


async def _handle_reload(page: Page) -> schemas.ReloadResponse:
    await page.reload()
    await page.wait_for_selector("#layaCanvas", timeout=PAGE_WAIT_TIMEOUT)
    return schemas.ReloadResponse()


async def _handle_quit() -> schemas.QuitResponse:
    return schemas.QuitResponse()


async def _handle_unknown(_req: Never) -> schemas.ErrorResponse:
    return schemas.ErrorResponse(message="unknown action")


def _request_handler_factory(
    page: Page,
    viewport: ViewportSize,
) -> core.RequestHandler:
    scale = _get_scale(viewport)

    async def handle_request(req: schemas.Request) -> schemas.Response:
        match req:
            case schemas.ResolutionRequest():
                res: schemas.Response = await _handle_resolution(
                    viewport,
                    scale,
                )
            case schemas.MoveMouseRequest():
                res = await _handle_move_mouse(page, req)
            case schemas.ClickMouseRequest():
                res = await _handle_click_mouse(page, req)
            case schemas.PressKeyRequest():
                res = await _handle_press_key(page, req)
            case schemas.TypeKeyRequest():
                res = await _handle_type_key(page, req)
            case schemas.ScreenshotRequest():
                res = await _handle_screenshot(page)
            case schemas.LogRequest():
                res = await _handle_log(page, req)
            case schemas.ReloadRequest():
                res = await _handle_reload(page)
            case schemas.QuitRequest():
                res = await _handle_quit()
            case _ as unknown:
                res = await _handle_unknown(unknown)
        return res

    return handle_request


async def _prepare_majsoul_page(page: Page, url: str) -> None:
    await page.goto(url)
    await page.wait_for_selector("#layaCanvas", timeout=PAGE_WAIT_TIMEOUT)


async def _get_spoofed_user_agent() -> str:
    async with (
        async_playwright() as p,
        await p.chromium.launch(headless=True) as browser,
        await browser.new_context() as context,
        await context.new_page() as page,
    ):
        await page.goto("https://www.google.com/")
        user_agent = await page.evaluate("navigator.userAgent")
        return user_agent.replace("HeadlessChrome", "Chrome")


async def run_browser_engine(
    config: Config,
    option: Option,
    server_runner: core.ServerRunner,
) -> None:
    browser_args = _create_browser_args(config, option)
    ignored_default_args = _create_ignored_default_args(option)
    viewport = _get_viewport_size(option)

    # If the user agent contains the string `HeadlessChrome`,
    # the browser will be rejected by Mahjong Soul's login process.
    # Therefore, when running in headless mode,
    # the user agent is spoofed.
    user_agent = await _get_spoofed_user_agent() if option.headless else None

    if option.user_data_dir is not None:
        async with (
            async_playwright() as p,
            await p.chromium.launch_persistent_context(
                user_data_dir=option.user_data_dir,
                args=browser_args,
                ignore_default_args=ignored_default_args,
                headless=option.headless,
                viewport=viewport,
                user_agent=user_agent,
            ) as context,
        ):
            if context.pages:
                page = context.pages[0]
                await _prepare_majsoul_page(page, option.url)
                request_handler = _request_handler_factory(page, viewport)
                await server_runner(config, request_handler)
            else:
                async with await context.new_page() as page:
                    await _prepare_majsoul_page(page, option.url)
                    request_handler = _request_handler_factory(page, viewport)
                    await server_runner(config, request_handler)
    else:
        # incognito mode
        async with (
            async_playwright() as p,
            await p.chromium.launch(
                args=browser_args,
                ignore_default_args=ignored_default_args,
                headless=option.headless,
            ) as browser,
            await browser.new_context(
                viewport=viewport,
                user_agent=user_agent,
            ) as context,
            await context.new_page() as page,
        ):
            await _prepare_majsoul_page(page, option.url)
            request_handler = _request_handler_factory(page, viewport)
            await server_runner(config, request_handler)
