# ruff: noqa: INP001, PLR2004
import argparse
import base64
import json
import time
from pathlib import Path
from subprocess import Popen
from typing import Final

import grpc  # type:ignore[import-untyped]
from playwright.sync_api import BrowserContext, sync_playwright

from majsoulrpa._impl.browser import (
    STD_HEIGHT,
    URL_MAJSOUL,
    validate_viewport_size,
)
from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2 import (
    BrowserResponse,
    Timeout,
)
from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2_grpc import GRPCServerStub
from majsoulrpa.common import validate_user_port

_SNIFFER_PATH: Final = Path(__file__).parents[1] / "_mitmproxy/sniffer.py"


def main(context: BrowserContext, db_port: int) -> None:  # noqa: PLR0915
    def respond(response: dict[str, str]) -> None:
        message = json.dumps(response, separators=(",", ":"))
        message_bytes = message.encode("utf-8")
        client.push_browser_response(BrowserResponse(content=message_bytes))

    with grpc.insecure_channel(f"localhost:{db_port}") as channel:
        client = GRPCServerStub(channel)

        page = context.new_page()
        page.goto(URL_MAJSOUL)
        page.wait_for_selector("#layaCanvas", timeout=60000)

        while True:
            request_bytes: bytes = client.pop_browser_request(
                Timeout(seconds=3600),
            ).content

            if request_bytes == b"":
                msg = "There have been no requests for an hour."
                raise TimeoutError(msg)

            request_str = request_bytes.decode(encoding="utf-8")
            request = json.loads(request_str)

            match request["type"]:
                case "refresh":
                    page.reload()
                    response = {"result": "O.K."}
                    respond(response)
                case "write":
                    text = request["text"]
                    delay = request["delay"]
                    if text != "":
                        page.keyboard.type(text, delay=delay)
                    response = {"result": "O.K."}
                    respond(response)
                case "press":
                    keys = request["keys"]
                    if isinstance(keys, str):
                        page.keyboard.press(keys)
                    else:
                        for k in keys:
                            page.keyboard.press(k)
                    response = {"result": "O.K."}
                    respond(response)
                case "press_hotkey":
                    args = request["args"]
                    keys = "+".join(args)
                    page.keyboard.press(keys)
                    response = {"result": "O.K."}
                    respond(response)
                case "scroll":
                    response = {"result": "Error: Not implemented."}
                    respond(response)
                case "click":
                    x = request["x"]
                    y = request["y"]
                    page.mouse.click(x, y)
                    response = {"result": "O.K."}
                    respond(response)
                case "get_screenshot":
                    data_png = page.screenshot()
                    data_b64 = base64.b64encode(data_png)
                    data = data_b64.decode("utf-8")
                    response = {"result": "O.K.", "data": data}
                    respond(response)
                case "close":
                    response = {"result": "O.K."}
                    respond(response)
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
    proxy_port: int = parser.parse_args().proxy_port
    db_port: int = parser.parse_args().db_port
    initial_left: int = parser.parse_args().initial_left
    initial_top: int = parser.parse_args().initial_top
    height: int = parser.parse_args().viewport_height
    validate_user_port(proxy_port)
    validate_user_port(db_port)
    if proxy_port == db_port:
        msg = f"Ports must be different. {proxy_port=}, {db_port=}"
        raise ValueError(msg)
    width = height * 16 // 9
    validate_viewport_size(width, height)

    # Run network sniffering process
    sniffer_args: list[str | Path] = [
        "mitmdump",
        "-qs",
        _SNIFFER_PATH,
        "--set",
        f"server_port={db_port}",
    ]

    with Popen(sniffer_args):  # noqa: S603
        time.sleep(10.0)

        proxy_server = f"--proxy-server=http://localhost:{proxy_port}"
        ignore_certifi_errors = "--ignore-certificate-errors"
        options = [proxy_server, ignore_certifi_errors]
        viewport_size = {"width": width, "height": height}
        mute_audio_off: list[str] | None = ["--mute-audio"]
        is_headless = False
        if False:
            mute_audio_off = None
            is_headless = True

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
