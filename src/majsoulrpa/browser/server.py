import argparse
import asyncio
import base64
import contextlib
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Never, Self

import zmq
import zmq.asyncio
from playwright.async_api import Page, ViewportSize, async_playwright

from majsoulrpa import netutils
from majsoulrpa.browser import schemas
from majsoulrpa.constants import (
    DEFAULT_CLIENT_ADDRESS,
    DEFAULT_PROXY_PORT,
    DEFAULT_REMOTE_PORT,
    DEFAULT_SNIFFER_PORT,
    DEFAULT_VIEWPORT_HEIGHT,
)
from majsoulrpa.exceptions import UserInputError
from majsoulrpa.sniffer import ADDON_PATH

MAJSOUL_URL = "https://game.mahjongsoul.com/"  # JP version


VIEWPORT_HEIGHT_CHOICES = (540, 720, 900, 1080, 1440)
PAGE_WAIT_TIMEOUT = 30000


@dataclass(frozen=True)
class CommandLineArgs:
    client_address: str = DEFAULT_CLIENT_ADDRESS
    remote_port: int = DEFAULT_REMOTE_PORT
    sniffer_port: int = DEFAULT_SNIFFER_PORT
    proxy_port: int = DEFAULT_PROXY_PORT

    window_left: int = 0
    window_top: int = 0
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT
    headless: bool = False
    user_data_dir: Path | None = None


def get_command_line_args() -> CommandLineArgs:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--client-address",
        type=str,
        default=DEFAULT_CLIENT_ADDRESS,
    )
    parser.add_argument(
        "--remote-port",
        type=int,
        default=DEFAULT_REMOTE_PORT,
    )
    parser.add_argument(
        "--sniffer-port",
        type=int,
        default=DEFAULT_SNIFFER_PORT,
    )
    parser.add_argument(
        "--proxy-port",
        type=int,
        default=DEFAULT_PROXY_PORT,
    )

    parser.add_argument("--window-left", type=int, default=0)
    parser.add_argument("--window-top", type=int, default=0)
    parser.add_argument(
        "--viewport-height",
        type=int,
        choices=VIEWPORT_HEIGHT_CHOICES,
        default=DEFAULT_VIEWPORT_HEIGHT,
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--user-data-dir", type=Path, default=None)

    args = parser.parse_args()

    return CommandLineArgs(
        client_address=args.client_address,
        remote_port=args.remote_port,
        sniffer_port=args.sniffer_port,
        proxy_port=args.proxy_port,
        window_left=args.window_left,
        window_top=args.window_top,
        viewport_height=args.viewport_height,
        headless=args.headless,
        user_data_dir=args.user_data_dir,
    )


@dataclass(frozen=True)
class Options:
    client_address: IPv4Address | IPv6Address
    remote_port: int
    sniffer_port: int
    proxy_port: int

    user_data_dir: Path | None
    browser_args: list[str]
    ignored_default_args: list[str]
    headless: bool
    viewport: ViewportSize
    scale: float

    @classmethod
    def from_args(cls, args: CommandLineArgs) -> Self:
        address = netutils.parse_ip_address(args.client_address)
        netutils.validate_user_port(args.remote_port)
        netutils.validate_user_port(args.sniffer_port)
        netutils.validate_user_port(args.proxy_port)

        ports = [args.remote_port, args.sniffer_port, args.proxy_port]
        if len(set(ports)) != len(ports):
            msg = "port number conflict"
            raise UserInputError(msg)

        user_data_dir = resolve_user_data_dir(args)
        browser_args = create_browser_args(args)
        ignored_default_args = create_ignored_default_args(args)
        viewport, scale = get_viewport_size(args)

        return cls(
            client_address=address,
            remote_port=args.remote_port,
            sniffer_port=args.sniffer_port,
            proxy_port=args.proxy_port,
            user_data_dir=user_data_dir,
            browser_args=browser_args,
            ignored_default_args=ignored_default_args,
            headless=args.headless,
            viewport=viewport,
            scale=scale,
        )


def resolve_user_data_dir(args: CommandLineArgs) -> Path | None:
    if args.user_data_dir is None:
        return None

    p = args.user_data_dir.resolve(strict=False)
    if p.exists():
        if p.is_file():
            msg = "invalid user-data-dir: file exists"
            raise UserInputError(msg)
    else:
        try:
            p.mkdir(parents=True)
        except (OSError, RuntimeError) as e:
            msg = "invalid user-data-dir"
            raise UserInputError(msg) from e

    return p


def create_browser_args(args: CommandLineArgs) -> list[str]:
    window_position = f"--window-position={args.window_left},{args.window_top}"
    proxy_server = f"--proxy-server=http://localhost:{args.proxy_port}"
    ignore_certificate_errors = "--ignore-certificate-errors"
    return [window_position, proxy_server, ignore_certificate_errors]


def create_ignored_default_args(args: CommandLineArgs) -> list[str]:
    return [] if args.headless else ["--mute-audio"]


def get_viewport_size(args: CommandLineArgs) -> tuple[ViewportSize, float]:
    height = args.viewport_height
    width = height * 16 // 9
    scale = height / DEFAULT_VIEWPORT_HEIGHT
    return ViewportSize(width=width, height=height), scale


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


async def run_server_inner(page: Page, options: Options) -> None:
    await page.goto(MAJSOUL_URL)
    await page.wait_for_selector("#layaCanvas", timeout=PAGE_WAIT_TIMEOUT)

    with zmq.asyncio.Context() as ctx, ctx.socket(zmq.REP) as socket:
        if options.client_address.version == 6:  # noqa: PLR2004
            socket.setsockopt(zmq.IPV6, 1)

        endpoint = netutils.make_endpoint(
            options.client_address,
            options.remote_port,
        )

        with socket.bind(f"tcp://{endpoint}"):
            while True:
                raw_req = await socket.recv_string()
                req = schemas.REQUEST_ADAPTER.validate_json(raw_req)

                match req:
                    case schemas.ResolutionRequest():
                        res: schemas.Response = await handle_resolution(
                            options.viewport,
                            options.scale,
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


async def run_server(options: Options) -> None:
    if options.user_data_dir is not None:
        async with (
            async_playwright() as p,
            await p.chromium.launch_persistent_context(
                user_data_dir=options.user_data_dir,
                args=options.browser_args,
                ignore_default_args=options.ignored_default_args,
                headless=options.headless,
            ) as context,
        ):
            if context.pages:
                page = context.pages[0]
                await run_server_inner(page, options)
            else:
                async with await context.new_page() as page:
                    await run_server_inner(page, options)
    else:
        # incognito mode
        async with (
            async_playwright() as p,
            await p.chromium.launch(
                args=options.browser_args,
                ignore_default_args=options.ignored_default_args,
                headless=options.headless,
            ) as browser,
            await browser.new_context(viewport=options.viewport) as context,
            await context.new_page() as page,
        ):
            await run_server_inner(page, options)


def wait_for_sniffer(
    port: int,
    timeout: float,
    connect_timeout: float,
    interval: float,
) -> None:
    address = ("localhost", port)
    start = time.time()

    while True:
        with (
            contextlib.suppress(TimeoutError, ConnectionRefusedError),
            socket.create_connection(address, connect_timeout),
        ):
            return

        if time.time() - start > timeout:
            msg = f"sniffer proxy localhost:{port} did not open within {timeout} seconds"  # noqa: E501
            raise TimeoutError(msg)

        time.sleep(interval)


def run_processes(options: Options) -> None:
    # Run network sniffering process
    sniffer_args: list[str | Path] = [
        "mitmdump",
        "-q",
        "-p",
        str(options.proxy_port),
        "-s",
        ADDON_PATH,
        "--set",
        f"address={options.client_address}",
        "--set",
        f"port={options.sniffer_port}",
    ]
    sniffer_process = subprocess.Popen(sniffer_args)  # noqa: S603
    wait_for_sniffer(options.proxy_port, 5.0, 0.5, 0.5)

    try:
        asyncio.run(run_server(options))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()


def main() -> None:
    try:
        args = get_command_line_args()
        options = Options.from_args(args)
        run_processes(options)
    except UserInputError as e:
        print(e, file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
