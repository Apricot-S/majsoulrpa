# ruff: noqa: PLR0913
import base64
import json
import random
import time
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from fractions import Fraction
from logging import getLogger
from typing import Any, Final

import grpc  # type:ignore[import-untyped]
import pywinctl as pwc
from playwright.sync_api import sync_playwright

from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2 import (
    BrowserRequest,
    Timeout,
    Void,
)
from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2_grpc import GRPCServerStub
from majsoulrpa.common import validate_user_port

logger = getLogger(__name__)

TITLE_MAJSOUL: Final[str] = "雀魂 -じゃんたま-| 麻雀を無料で気軽に"
URL_MAJSOUL: Final[str] = "https://game.mahjongsoul.com/"

STD_WIDTH: Final[int] = 1920
STD_HEIGHT: Final[int] = 1080
MIN_WIDTH: Final[int] = STD_WIDTH * 2 // 3
MIN_HEIGHT: Final[int] = STD_HEIGHT * 2 // 3
MAX_WIDTH: Final[int] = STD_WIDTH * 2
MAX_HEIGHT: Final[int] = STD_HEIGHT * 2

ASPECT_RATIO: Final[Fraction] = Fraction(16, 9)


def validate_viewport_size(width: int, height: int) -> None:
    if (
        width < MIN_WIDTH
        or width > MAX_WIDTH
        or height < MIN_HEIGHT
        or height > MAX_HEIGHT
        or Fraction(width, height) != ASPECT_RATIO
    ):
        msg = (
            "Supported viewport sizes are "
            f"from {MIN_WIDTH} x {MIN_HEIGHT} "
            f"to {MAX_WIDTH} x {MAX_HEIGHT} and 16:9 aspect ratio."
        )
        raise ValueError(msg)


def validate_region(
    left: int,
    top: int,
    width: int,
    height: int,
    viewport_width: int,
    viewport_height: int,
) -> None:
    if (
        left < 0
        or top < 0
        or width <= 0
        or height <= 0
        or left >= viewport_width
        or top >= viewport_height
        or width > (viewport_width - left)
        or height > (viewport_height - top)
    ):
        msg = (
            "A click was requested into an invalid area."
            f" {left=}, {top=}, {width=}, {height=}"
        )
        raise ValueError(msg)


def _get_random_point_in_region(
    left: int,
    top: int,
    width: int,
    height: int,
    edge_sigma: float = 0.2,
) -> tuple[int, int]:
    """Return random point in region.

    This function does not validate parameters.
    """

    def _get_point_impl(distance_origin: int, length_region: int) -> int:
        mu = distance_origin + length_region / 2.0
        sigma = (mu - distance_origin) / edge_sigma
        while True:
            p = random.normalvariate(mu, sigma)
            p = round(p)
            if distance_origin < p and p < (distance_origin + length_region):
                break
        return p

    x = _get_point_impl(left, width)
    y = _get_point_impl(top, height)

    return (x, y)


class BrowserBase(metaclass=ABCMeta):
    def check_single(self) -> None:
        """Check if only one target window exists.

        Throws a runtime error if the target does not exist or
        if two or more targets exist.
        """
        windows = [
            w for w in pwc.getAllWindows() if w.title.startswith(TITLE_MAJSOUL)
        ]
        if len(windows) == 0:
            msg = "No window for Mahjong Soul is found."
            raise RuntimeError(msg)
        if len(windows) > 1:
            msg = "Multiple windows for Mahjong Soul are found."
            raise RuntimeError(msg)

    @property
    @abstractmethod
    def zoom_ratio(self) -> float:
        pass

    @abstractmethod
    def refresh(self) -> None:
        pass

    @abstractmethod
    def write(self, text: str, delay: float | None = None) -> None:
        pass

    @abstractmethod
    def press(self, keys: str | Iterable[str]) -> None:
        pass

    @abstractmethod
    def press_hotkey(self, *args: str) -> None:
        pass

    @abstractmethod
    def scroll(self, clicks: int) -> None:
        pass

    @abstractmethod
    def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        pass

    @abstractmethod
    def get_screenshot(self) -> bytes:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class DesktopBrowser(BrowserBase):
    def __init__(
        self,
        *,
        proxy_port: int = 8080,
        initial_left: int = 0,
        initial_top: int = 0,
        width: int = STD_WIDTH,
        height: int = STD_HEIGHT,
    ) -> None:
        super().__init__()
        validate_user_port(proxy_port)
        validate_viewport_size(width, height)
        self._viewport_size = {"width": width, "height": height}
        self._zoom_ratio = width / STD_WIDTH

        initial_position = f"--window-position={initial_left},{initial_top}"
        proxy_server = f"--proxy-server=http://localhost:{proxy_port}"
        ignore_certifi_errors = "--ignore-certificate-errors"
        options = [initial_position, proxy_server, ignore_certifi_errors]

        self._context_manager = sync_playwright()
        self._browser = self._context_manager.start().chromium.launch(
            args=options,
            ignore_default_args=["--mute-audio"],
            headless=False,
        )
        self._context = self._browser.new_context(viewport=self._viewport_size)  # type: ignore[arg-type]
        self._page = self._context.new_page()
        self._page.goto(URL_MAJSOUL)

    @property
    def zoom_ratio(self) -> float:
        return self._zoom_ratio

    def refresh(self) -> None:
        self._page.reload()

    def write(self, text: str, delay: float | None = None) -> None:
        self._page.keyboard.type(text, delay=delay)

    def press(self, keys: str | Iterable[str]) -> None:
        if isinstance(keys, str):
            self._page.keyboard.press(keys)
        else:
            for k in keys:
                self._page.keyboard.press(k)

    def press_hotkey(self, *args: str) -> None:
        keys = "+".join(args)
        self._page.keyboard.press(keys)

    def scroll(self, clicks: int) -> None:
        if clicks == 0:
            return

        if clicks > 0:
            delta = 58 * 2
        else:
            logger.debug("scroll clicks is smaller than 0.")
            assert clicks < 0  # noqa: S101
            delta = -58 * 2
            clicks = abs(clicks)

        self._page.mouse.wheel(delta_x=0, delta_y=delta)
        for _ in range(clicks - 1):
            time.sleep(0.1)
            self._page.mouse.wheel(delta_x=0, delta_y=delta)

    def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        validate_region(
            left,
            top,
            width,
            height,
            self._viewport_size["width"],
            self._viewport_size["height"],
        )
        if edge_sigma <= 0.0:  # noqa: PLR2004
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = _get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )
        self._page.mouse.click(x, y)

    def get_screenshot(self) -> bytes:
        """Return bytes in png format."""
        return self._page.screenshot()

    def close(self) -> None:
        self._context.close()
        self._browser.close()
        self._context_manager.__exit__()


class RemoteBrowser(BrowserBase):
    def __init__(
        self,
        *,
        db_port: int = 37247,
        width: int = STD_WIDTH,
        height: int = STD_HEIGHT,
    ) -> None:
        super().__init__()
        validate_viewport_size(width, height)
        self._viewport_size = {"width": width, "height": height}
        self._zoom_ratio = width / STD_WIDTH

        self._channel = grpc.insecure_channel(f"localhost:{db_port}")
        self._client = GRPCServerStub(self._channel)

    def check_single(self) -> None:
        pass

    @property
    def zoom_ratio(self) -> float:
        return self._zoom_ratio

    def _communicate(self, request: object) -> dict[str, Any]:
        request = json.dumps(request, separators=(",", ":"))
        request = request.encode("UTF-8")

        num_request: int = self._client.len_browser_request(Void()).size
        if num_request > 0:
            msg = (
                "Failed to send a message to the remote browser.:"
                " The previous request remains."
            )
            raise RuntimeError(msg)

        self._client.push_browser_request(BrowserRequest(content=request))

        num_request = self._client.len_browser_request(Void()).size
        if num_request == 0:
            msg = (
                "Failed to send a message to the remote browser.:"
                " The request queue is empty."
            )
            raise RuntimeError(msg)
        if num_request > 1:
            msg = (
                "Failed to send a message to the remote browser.:"
                f" There are {num_request} requests in the queue."
            )
            raise RuntimeError(msg)

        response_bytes: bytes = self._client.pop_browser_response(
            Timeout(seconds=10),
        ).content

        if response_bytes == b"":
            msg = "Failed to receive response within the timeout period."
            raise TimeoutError(msg)

        response = response_bytes.decode("UTF-8")
        return json.loads(response)

    @staticmethod
    def _check_response(response: dict[str, object]) -> None:
        if response["result"] != "O.K.":
            msg = "Failed to send a message to the remote browser."
            raise RuntimeError(msg)

    def refresh(self) -> None:
        request = {"type": "fullscreen"}
        response = self._communicate(request)
        self._check_response(response)

    def write(self, text: str, delay: float | None = None) -> None:
        request = {"type": "write", "text": text, "delay": delay}
        response = self._communicate(request)
        self._check_response(response)

    def press(self, keys: str | Iterable[str]) -> None:
        if not isinstance(keys, str):
            keys = list(keys)
        request = {"type": "press", "keys": keys}
        response = self._communicate(request)
        self._check_response(response)

    def press_hotkey(self, *args: str) -> None:
        request = {"type": "press_hotkey", "args": list(args)}
        response = self._communicate(request)
        self._check_response(response)

    def scroll(self, clicks: int) -> None:
        request = {"type": "scroll", "clicks": clicks}
        response = self._communicate(request)
        self._check_response(response)

    def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        validate_region(
            left,
            top,
            width,
            height,
            self._viewport_size["width"],
            self._viewport_size["height"],
        )
        if edge_sigma <= 0.0:  # noqa: PLR2004
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = _get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )

        request = {"type": "click", "x": x, "y": y}
        response = self._communicate(request)
        self._check_response(response)

    def get_screenshot(self) -> bytes:
        request = {"type": "get_screenshot"}
        response = self._communicate(request)
        self._check_response(response)
        data: str = response["data"]
        return base64.b64decode(data)

    def close(self) -> None:
        self._channel.close()
