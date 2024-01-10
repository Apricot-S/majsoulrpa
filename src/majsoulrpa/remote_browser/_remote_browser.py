#!/usr/bin/env python3
# ruff: noqa: PLR0913, PLR2004
import argparse
import base64
from pathlib import Path
from subprocess import Popen
from typing import Final

import zmq
from playwright.sync_api import BrowserContext, sync_playwright
from zmq.utils.win32 import allow_interrupt

from majsoulrpa._impl.browser import (
    ASPECT_RATIO,
    STD_HEIGHT,
    URL_MAJSOUL,
    validate_viewport_size,
)
from majsoulrpa.common import validate_user_port

_SNIFFER_PATH: Final = Path(__file__).parents[1] / "_mitmproxy/sniffer.py"


def parse_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote_port", type=int, default=19222)
    parser.add_argument("--proxy_port", type=int, default=8080)
    parser.add_argument("--message_queue_port", type=int, default=37247)
    parser.add_argument("--initial_left", type=int, default=0)
    parser.add_argument("--initial_top", type=int, default=0)
    parser.add_argument("--viewport_height", type=int, default=STD_HEIGHT)
    parser.add_argument("--headless", action="store_true")
    return parser.parse_args()


def validate_options(
    remote_port: int,
    proxy_port: int,
    message_queue_port: int,
    width: int,
    height: int,
) -> None:
    validate_user_port(remote_port)
    validate_user_port(proxy_port)
    validate_user_port(message_queue_port)
    if len({remote_port, proxy_port, message_queue_port}) != 3:
        msg = (
            "Ports must be different. "
            f"{remote_port=}, {proxy_port=}, {message_queue_port=}"
        )
        raise ValueError(msg)
    validate_viewport_size(width, height)


def _launch_remote_browser_core(  # noqa: PLR0915
    browser_context: BrowserContext,
    remote_port: int,
) -> None:
    page = browser_context.new_page()
    page.goto(URL_MAJSOUL)
    page.wait_for_selector("#layaCanvas", timeout=60000)

    with (
        zmq.Context() as remote_context,
        remote_context.socket(zmq.REP) as socket,
        socket.bind(f"tcp://127.0.0.1:{remote_port}"),
    ):
        poller_in = zmq.Poller()
        poller_in.register(socket, zmq.POLLIN)

        def interrupt_polling() -> None:
            poller_in.unregister(socket)
            socket.close()
            remote_context.destroy()

        while True:
            with allow_interrupt(interrupt_polling):
                if poller_in.poll(300_000):
                    request = socket.recv_json()
                else:
                    msg = "Failed to receive a message from the RPA client."
                    raise TimeoutError(msg)
                if not isinstance(request, dict):
                    raise TypeError
                if any(not isinstance(key, str) for key in request):
                    raise TypeError

            match request["type"]:
                case "refresh":
                    page.reload()
                    response = {"result": "O.K."}
                    socket.send_json(response)
                case "write":
                    text = request["text"]
                    delay = request["delay"]
                    if text != "":
                        page.keyboard.type(text, delay=delay)
                    response = {"result": "O.K."}
                    socket.send_json(response)
                case "press":
                    keys = request["keys"]
                    if isinstance(keys, str):
                        page.keyboard.press(keys)
                    else:
                        for k in keys:
                            page.keyboard.press(k)
                    response = {"result": "O.K."}
                    socket.send_json(response)
                case "press_hotkey":
                    args = request["args"]
                    keys = "+".join(args)
                    page.keyboard.press(keys)
                    response = {"result": "O.K."}
                    socket.send_json(response)
                case "scroll":
                    response = {"result": "Error: Not implemented."}
                    socket.send_json(response)
                case "click":
                    x = request["x"]
                    y = request["y"]
                    page.mouse.click(x, y)
                    response = {"result": "O.K."}
                    socket.send_json(response)
                case "get_screenshot":
                    data_png = page.screenshot()
                    data_b64 = base64.b64encode(data_png)
                    data = data_b64.decode("utf-8")
                    response = {"result": "O.K.", "data": data}
                    socket.send_json(response)
                case "close":
                    response = {"result": "O.K."}
                    socket.send_json(response)
                    break
                case _ as unexpected:
                    msg = f"{unexpected}: An unknown message."
                    raise RuntimeError(msg)


def launch_remote_browser(
    remote_port: int,
    proxy_port: int,
    message_queue_port: int,
    initial_left: int,
    initial_top: int,
    width: int,
    height: int,
    *,
    is_headless: bool,
) -> None:
    validate_options(
        remote_port,
        proxy_port,
        message_queue_port,
        width,
        height,
    )

    # Run network sniffering process
    sniffer_args: list[str | Path] = [
        "mitmdump",
        "-qs",
        _SNIFFER_PATH,
        "--set",
        f"server_port={message_queue_port}",
    ]

    sniffer_process = Popen(sniffer_args)  # noqa: S603
    try:
        initial_position = f"--window-position={initial_left},{initial_top}"
        proxy_server = f"--proxy-server=http://localhost:{proxy_port}"
        ignore_certifi_errors = "--ignore-certificate-errors"
        options = [initial_position, proxy_server, ignore_certifi_errors]
        viewport_size = {"width": width, "height": height}
        mute_audio_off: list[str] | None = ["--mute-audio"]
        if is_headless:
            mute_audio_off = None

        with (
            sync_playwright() as playwright,
            playwright.chromium.launch(
                args=options,
                ignore_default_args=mute_audio_off,
                headless=is_headless,
            ) as browser,
            browser.new_context(viewport=viewport_size) as context,  # type: ignore[arg-type]
        ):
            _launch_remote_browser_core(context, remote_port)
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()


def main() -> None:
    args = parse_options()

    remote_port: int = args.remote_port
    proxy_port: int = args.proxy_port
    message_queue_port: int = args.message_queue_port
    initial_left: int = args.initial_left
    initial_top: int = args.initial_top
    height: int = args.viewport_height
    is_headless: bool = args.headless

    width = int(height * ASPECT_RATIO)

    launch_remote_browser(
        remote_port,
        proxy_port,
        message_queue_port,
        initial_left,
        initial_top,
        width,
        height,
        is_headless=is_headless,
    )


if __name__ == "__main__":
    main()
