#!/usr/bin/env python3
# ruff: noqa: INP001, PLR2004
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


def main(browser_context: BrowserContext, db_port: int) -> None:  # noqa: PLR0915
    page = browser_context.new_page()
    page.goto(URL_MAJSOUL)
    page.wait_for_selector("#layaCanvas", timeout=60000)

    with (
        zmq.Context() as remote_context,
        remote_context.socket(zmq.REP) as socket,
        socket.bind(f"tcp://127.0.0.1:{db_port}"),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy_port", type=int, default=8080)
    parser.add_argument("--db_port", type=int, default=37247)
    parser.add_argument("--initial_left", type=int, default=0)
    parser.add_argument("--initial_top", type=int, default=0)
    parser.add_argument("--viewport_height", type=int, default=STD_HEIGHT)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    proxy_port: int = args.proxy_port
    db_port: int = args.db_port
    initial_left: int = args.initial_left
    initial_top: int = args.initial_top
    height: int = args.viewport_height
    is_headless: bool = args.headless

    validate_user_port(proxy_port)
    validate_user_port(db_port)
    if proxy_port == db_port:
        msg = f"Ports must be different. {proxy_port=}, {db_port=}"
        raise ValueError(msg)
    width = int(height * ASPECT_RATIO)
    validate_viewport_size(width, height)

    # Run network sniffering process
    sniffer_args: list[str | Path] = [
        "mitmdump",
        "-qs",
        _SNIFFER_PATH,
        "--set",
        f"server_port={db_port + 1}",
    ]

    sniffer_process = Popen(sniffer_args)  # noqa: S603
    try:
        proxy_server = f"--proxy-server=http://localhost:{proxy_port}"
        ignore_certifi_errors = "--ignore-certificate-errors"
        options = [proxy_server, ignore_certifi_errors]
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
            main(context, db_port)
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()
