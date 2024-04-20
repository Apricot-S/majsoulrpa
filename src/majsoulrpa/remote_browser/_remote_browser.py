#!/usr/bin/env python3
# ruff: noqa: PLR2004
import argparse
import base64
from ipaddress import ip_address
from pathlib import Path
from subprocess import Popen
from time import sleep
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


def parse_option() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote_host", type=str, default="127.0.0.1")
    parser.add_argument("--remote_port", type=int, default=19222)
    parser.add_argument("--proxy_port", type=int, default=8080)
    parser.add_argument("--message_queue_port", type=int, default=37247)
    parser.add_argument("--initial_left", type=int, default=0)
    parser.add_argument("--initial_top", type=int, default=0)
    parser.add_argument("--viewport_height", type=int, default=STD_HEIGHT)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--headless", action="store_true")
    return parser.parse_args()


def validate_option(
    remote_host: str,
    remote_port: int,
    proxy_port: int,
    message_queue_port: int,
    viewport_height: int,
    timeout: int,
) -> None:
    ip_address(remote_host)
    validate_user_port(remote_port)
    validate_user_port(proxy_port)
    validate_user_port(message_queue_port)
    if len({remote_port, proxy_port, message_queue_port}) != 3:
        msg = (
            "Ports must be different. "
            f"{remote_port=}, {proxy_port=}, {message_queue_port=}"
        )
        raise ValueError(msg)
    viewport_width = int(viewport_height * ASPECT_RATIO)
    validate_viewport_size(viewport_width, viewport_height)
    if timeout <= 0:
        msg = "Timeout must be a positive integer."
        raise ValueError(msg)


def _launch_remote_browser_core(
    browser_context: BrowserContext,
    remote_host: str,
    remote_port: int,
    viewport_size: dict[str, int],
    timeout: int,
) -> None:
    zoom_ratio = viewport_size["height"] / STD_HEIGHT

    page = browser_context.new_page()
    page.goto(URL_MAJSOUL)
    page.wait_for_selector("#layaCanvas", timeout=60000)

    with (
        zmq.Context() as remote_context,
        remote_context.socket(zmq.REP) as socket,
        socket.bind(f"tcp://{remote_host}:{remote_port}"),
    ):
        poller_in = zmq.Poller()
        poller_in.register(socket, zmq.POLLIN)

        def interrupt_polling() -> None:
            poller_in.unregister(socket)
            socket.close()
            remote_context.destroy()

        while True:
            with allow_interrupt(interrupt_polling):
                if poller_in.poll(timeout * 1000):
                    request = socket.recv_json()
                else:
                    print(  # noqa: T201
                        "There was no operation from the RPA client "
                        "until the timeout.",
                    )
                    break

            if not isinstance(request, dict):
                msg = "An invalid message was received."
                raise TypeError(msg)
            if any(not isinstance(key, str) for key in request):
                msg = "An invalid message was received."
                raise TypeError(msg)

            match request["type"]:
                case "zoom_ratio":
                    response = {"result": "O.K.", "data": zoom_ratio}
                    socket.send_json(response)
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
                case "move":
                    x = request["x"]
                    y = request["y"]
                    page.mouse.move(x, y)
                    response = {"result": "O.K."}
                    socket.send_json(response)
                case "scroll":
                    response = {"result": "Error: Not implemented."}
                    socket.send_json(response)
                case "_get_viewport_size":
                    response = {"result": "O.K.", "data": viewport_size}
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
    remote_host: str = "127.0.0.1",
    remote_port: int = 19222,
    proxy_port: int = 8080,
    message_queue_port: int = 37247,
    initial_left: int = 0,
    initial_top: int = 0,
    viewport_height: int = 1080,
    timeout: int = 600,
    *,
    headless: bool = False,
) -> None:
    validate_option(
        remote_host,
        remote_port,
        proxy_port,
        message_queue_port,
        viewport_height,
        timeout,
    )
    viewport_width = int(viewport_height * ASPECT_RATIO)

    # Run network sniffering process
    sniffer_args: list[str | Path] = [
        "mitmdump",
        "-qs",
        _SNIFFER_PATH,
        "--set",
        f"host={remote_host}",
        "--set",
        f"port={message_queue_port}",
    ]

    sniffer_process = Popen(sniffer_args)  # noqa: S603
    # After starting the sniffer process, if the browser is launched
    # immediately, there may be cases where the browser attempts to
    # connect to the proxy port before the sniffer process begins
    # listening on it. As a result, the browser may fail to connect to
    # the proxy (sniffer) and throw a `net::ERR_PROXY_CONNECTION_FAILED`
    # exception. The following `sleep` is to avoid this problem, by
    # waiting for a while after starting the sniffer process before
    # initiating the launch of the browser.
    sleep(1.0)
    try:
        initial_position = f"--window-position={initial_left},{initial_top}"
        proxy_server = f"--proxy-server=http://localhost:{proxy_port}"
        ignore_certifi_errors = "--ignore-certificate-errors"
        options = [initial_position, proxy_server, ignore_certifi_errors]
        viewport_size = {"width": viewport_width, "height": viewport_height}
        mute_audio_off = None if headless else ["--mute-audio"]

        with (
            sync_playwright() as playwright,
            playwright.chromium.launch(
                args=options,
                ignore_default_args=mute_audio_off,
                headless=headless,
            ) as browser,
            browser.new_context(viewport=viewport_size) as context,  # type: ignore[arg-type]
        ):
            _launch_remote_browser_core(
                context,
                remote_host,
                remote_port,
                viewport_size,
                timeout,
            )
            input("Type something to close the remote browser.")
    except KeyboardInterrupt:
        pass
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()


def main() -> None:
    args = parse_option()

    remote_host: str = args.remote_host
    remote_port: int = args.remote_port
    proxy_port: int = args.proxy_port
    message_queue_port: int = args.message_queue_port
    initial_left: int = args.initial_left
    initial_top: int = args.initial_top
    viewport_height: int = args.viewport_height
    timeout: int = args.timeout
    headless: bool = args.headless

    launch_remote_browser(
        remote_host,
        remote_port,
        proxy_port,
        message_queue_port,
        initial_left,
        initial_top,
        viewport_height,
        timeout,
        headless=headless,
    )


if __name__ == "__main__":
    main()
