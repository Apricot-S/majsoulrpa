import asyncio
import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Never

from playwright.async_api import Page, ViewportSize, async_playwright

from majsoulrpa.browser import schemas
from majsoulrpa.browser.server.config import Config
from majsoulrpa.browser.server.core import RequestHandler, start_server
from majsoulrpa.browser.server.sniffer import run_sniffer
from majsoulrpa.constants import DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.exceptions import UserInputError
from majsoulrpa.sniffer import ADDON_PATH

MAJSOUL_URL = "https://game.mahjongsoul.com/"  # JP version

PAGE_WAIT_TIMEOUT = 30000


@dataclass(frozen=True)
class Option:
    user_data_dir: Path | None
    window_left: int
    window_top: int
    viewport_height: int
    headless: bool

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


def _get_viewport_size(option: Option) -> tuple[ViewportSize, float]:
    height = option.viewport_height
    width = height * 16 // 9
    scale = height / DEFAULT_VIEWPORT_HEIGHT
    return ViewportSize(width=width, height=height), scale


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
    scale: float,
) -> RequestHandler:
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
            case schemas.ReloadRequest():
                res = await _handle_reload(page)
            case schemas.QuitRequest():
                res = await _handle_quit()
            case _ as unknown:
                res = await _handle_unknown(unknown)
        return res

    return handle_request


async def _prepare_majsoul_page(page: Page) -> None:
    await page.goto(MAJSOUL_URL)
    await page.wait_for_selector("#layaCanvas", timeout=PAGE_WAIT_TIMEOUT)


async def run_server(config: Config, option: Option) -> None:
    browser_args = _create_browser_args(config, option)
    ignored_default_args = _create_ignored_default_args(option)
    viewport, scale = _get_viewport_size(option)

    if option.user_data_dir is not None:
        async with (
            async_playwright() as p,
            await p.chromium.launch_persistent_context(
                user_data_dir=option.user_data_dir,
                args=browser_args,
                ignore_default_args=ignored_default_args,
                headless=option.headless,
                viewport=viewport,
            ) as context,
        ):
            if context.pages:
                page = context.pages[0]
                await _prepare_majsoul_page(page)
                request_handler = _request_handler_factory(
                    page,
                    viewport,
                    scale,
                )
                await start_server(config, request_handler)
            else:
                async with await context.new_page() as page:
                    await _prepare_majsoul_page(page)
                    request_handler = _request_handler_factory(
                        page,
                        viewport,
                        scale,
                    )
                    await start_server(config, request_handler)
    else:
        # incognito mode
        async with (
            async_playwright() as p,
            await p.chromium.launch(
                args=browser_args,
                ignore_default_args=ignored_default_args,
                headless=option.headless,
            ) as browser,
            await browser.new_context(viewport=viewport) as context,
            await context.new_page() as page,
        ):
            await _prepare_majsoul_page(page)
            request_handler = _request_handler_factory(page, viewport, scale)
            await start_server(config, request_handler)


def run_processes(config: Config, option: Option) -> None:
    sniffer_process = run_sniffer(config, ADDON_PATH)

    try:
        asyncio.run(run_server(config, option))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()
