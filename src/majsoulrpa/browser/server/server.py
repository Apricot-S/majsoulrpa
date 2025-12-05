import asyncio
import base64
from typing import Never

import zmq
import zmq.asyncio
from playwright.async_api import Page, ViewportSize, async_playwright

from majsoulrpa import netutils
from majsoulrpa.browser import schemas
from majsoulrpa.browser.server.config import Config
from majsoulrpa.browser.server.engine import (
    Option,
    _create_browser_args,
    _create_ignored_default_args,
    _get_viewport_size,
)
from majsoulrpa.browser.server.sniffer import run_sniffer
from majsoulrpa.sniffer import ADDON_PATH

MAJSOUL_URL = "https://game.mahjongsoul.com/"  # JP version


VIEWPORT_HEIGHT_CHOICES = (540, 720, 900, 1080, 1440)
PAGE_WAIT_TIMEOUT = 30000


async def handle_resolution(
    viewport: ViewportSize,
    scale: float,
) -> schemas.ResolutionResponse:
    return schemas.ResolutionResponse(
        width=viewport["width"],
        height=viewport["height"],
        scale=scale,
    )


async def handle_move_mouse(
    page: Page,
    req: schemas.MoveMouseRequest,
) -> schemas.MoveMouseResponse:
    x = req.x
    y = req.y
    await page.mouse.move(x=x, y=y)
    return schemas.MoveMouseResponse(x=x, y=y)


async def handle_click_mouse(
    page: Page,
    req: schemas.ClickMouseRequest,
) -> schemas.ClickMouseResponse:
    x = req.x
    y = req.y
    delay = req.delay
    await page.mouse.click(x=x, y=y, delay=delay)
    return schemas.ClickMouseResponse(x=x, y=y, delay=delay)


async def handle_press_key(
    page: Page,
    req: schemas.PressKeyRequest,
) -> schemas.PressKeyResponse:
    key = req.key
    delay = req.delay
    await page.keyboard.press(key=key, delay=delay)
    return schemas.PressKeyResponse(key=key, delay=delay)


async def handle_type_key(
    page: Page,
    req: schemas.TypeKeyRequest,
) -> schemas.TypeKeyResponse:
    text = req.text
    delay = req.delay
    await page.keyboard.type(text=text, delay=delay)
    return schemas.TypeKeyResponse(text=text, delay=delay)


async def handle_screenshot(page: Page) -> schemas.ScreenshotResponse:
    image = await page.screenshot()
    image_b64 = base64.b64encode(image).decode(encoding="utf-8")
    return schemas.ScreenshotResponse(image=image_b64)


async def handle_reload(page: Page) -> schemas.ReloadResponse:
    await page.reload()
    await page.wait_for_selector("#layaCanvas", timeout=PAGE_WAIT_TIMEOUT)
    return schemas.ReloadResponse()


async def handle_quit() -> schemas.QuitResponse:
    return schemas.QuitResponse()


async def handle_unknown(_req: Never) -> schemas.ErrorResponse:
    return schemas.ErrorResponse(message="unknown action")


async def run_server_inner(
    page: Page,
    config: Config,
    viewport: ViewportSize,
    scale: float,
) -> None:
    await page.goto(MAJSOUL_URL)
    await page.wait_for_selector("#layaCanvas", timeout=PAGE_WAIT_TIMEOUT)

    with zmq.asyncio.Context() as ctx, ctx.socket(zmq.REP) as socket:
        if config.client_address.version == 6:  # noqa: PLR2004
            socket.setsockopt(zmq.IPV6, 1)

        endpoint = netutils.make_endpoint(
            config.client_address,
            config.remote_port,
        )

        with socket.bind(f"tcp://{endpoint}"):
            while True:
                raw_req = await socket.recv_string()
                req = schemas.REQUEST_ADAPTER.validate_json(raw_req)

                match req:
                    case schemas.ResolutionRequest():
                        res: schemas.Response = await handle_resolution(
                            viewport,
                            scale,
                        )
                    case schemas.MoveMouseRequest():
                        res = await handle_move_mouse(page, req)
                    case schemas.ClickMouseRequest():
                        res = await handle_click_mouse(page, req)
                    case schemas.PressKeyRequest():
                        res = await handle_press_key(page, req)
                    case schemas.TypeKeyRequest():
                        res = await handle_type_key(page, req)
                    case schemas.ScreenshotRequest():
                        res = await handle_screenshot(page)
                    case schemas.ReloadRequest():
                        res = await handle_reload(page)
                    case schemas.QuitRequest():
                        res = await handle_quit()
                        await socket.send_string(res.model_dump_json())
                        break
                    case _ as unknown:
                        res = await handle_unknown(unknown)

                await socket.send_string(res.model_dump_json())


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
                await run_server_inner(page, config, viewport, scale)
            else:
                async with await context.new_page() as page:
                    await run_server_inner(page, config, viewport, scale)
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
            await run_server_inner(page, config, viewport, scale)


def run_processes(config: Config, option: Option) -> None:
    sniffer_process = run_sniffer(config, ADDON_PATH)

    try:
        asyncio.run(run_server(config, option))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()
