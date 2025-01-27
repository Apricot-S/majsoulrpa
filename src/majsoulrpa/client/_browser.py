import asyncio
import base64
import json
import random
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from fractions import Fraction
from ipaddress import ip_address
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

import zmq
import zmq.asyncio
from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    ViewportSize,
    async_playwright,
)

from ._validation import validate_user_port

if TYPE_CHECKING:
    from playwright.async_api._context_manager import PlaywrightContextManager

logger = getLogger(__name__)

URL_MAJSOUL: Final[str] = "https://game.mahjongsoul.com/"

STD_WIDTH: Final[int] = 1920
STD_HEIGHT: Final[int] = 1080
MIN_WIDTH: Final[int] = STD_WIDTH * 2 // 3
MIN_HEIGHT: Final[int] = STD_HEIGHT * 2 // 3
MAX_WIDTH: Final[int] = STD_WIDTH * 2
MAX_HEIGHT: Final[int] = STD_HEIGHT * 2
ASPECT_RATIO: Final[Fraction] = Fraction(16, 9)

MAX_LATENCY: Final[int] = 2_000  # ms


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
            if distance_origin < p < (distance_origin + length_region):
                break
        return p

    x = _get_point_impl(left, width)
    y = _get_point_impl(top, height)

    return (x, y)


class BrowserBase(metaclass=ABCMeta):
    @abstractmethod
    async def get_zoom_ratio(self) -> float:
        pass

    @abstractmethod
    async def refresh(self) -> None:
        pass

    @abstractmethod
    async def write(self, text: str, delay: float | None = None) -> None:
        pass

    @abstractmethod
    async def press(self, keys: str | Iterable[str]) -> None:
        pass

    @abstractmethod
    async def press_hotkey(self, *args: str) -> None:
        pass

    @abstractmethod
    async def move_to_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        pass

    @abstractmethod
    async def scroll(self, clicks: int) -> None:
        pass

    @abstractmethod
    async def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        pass

    @abstractmethod
    async def get_screenshot(self) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class DesktopBrowser(BrowserBase):
    def __init__(
        self,
        proxy_port: int = 8080,
        initial_left: int = 0,
        initial_top: int = 0,
        width: int = STD_WIDTH,
        height: int = STD_HEIGHT,
        *,
        headless: bool = False,
        user_data_dir: str | Path | None = None,
    ) -> None:
        super().__init__()
        validate_user_port(proxy_port)
        validate_viewport_size(width, height)
        self._viewport_size = ViewportSize(width=width, height=height)
        self._zoom_ratio = height / STD_HEIGHT

        self._proxy_port = proxy_port
        self._initial_left = initial_left
        self._initial_top = initial_top
        self._headless = headless
        self._user_data_dir = user_data_dir

        self._context_manager: PlaywrightContextManager | None = None
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def launch(self) -> None:
        self._context_manager = async_playwright()
        self._playwright = await self._context_manager.start()

        initial_position = (
            f"--window-position={self._initial_left},{self._initial_top}"
        )
        proxy_server = f"--proxy-server=http://localhost:{self._proxy_port}"
        ignore_certifi_errors = "--ignore-certificate-errors"
        options = [
            initial_position,
            proxy_server,
            ignore_certifi_errors,
        ]
        mute_audio_off = None if self._headless else ["--mute-audio"]

        if self._user_data_dir is not None:
            self._context = (
                await self._playwright.chromium.launch_persistent_context(
                    self._user_data_dir,
                    args=options,
                    ignore_default_args=mute_audio_off,
                    headless=self._headless,
                    viewport=self._viewport_size,
                )
            )
            self._page = self._context.pages[0]
        else:
            self._browser = await self._playwright.chromium.launch(
                args=options,
                ignore_default_args=mute_audio_off,
                headless=self._headless,
            )
            self._context = await self._browser.new_context(
                viewport=self._viewport_size,
            )
            self._page = await self._context.new_page()

        await self._page.goto(URL_MAJSOUL)

    def is_launched(self) -> bool:
        if self._context_manager is None:
            return False
        if self._playwright is None:
            return False
        if self._context is None:
            return False
        return self._page is not None

    def _assert_launched(self) -> None:
        if not self.is_launched():
            msg = "The browser has not been launched."
            raise RuntimeError(msg)

    async def get_zoom_ratio(self) -> float:
        return self._zoom_ratio

    async def refresh(self) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        await self._page.reload()

    async def write(self, text: str, delay: float | None = None) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        await self._page.keyboard.type(text, delay=delay)

    async def press(self, keys: str | Iterable[str]) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101

        if isinstance(keys, str):
            await self._page.keyboard.press(keys)
        else:
            for k in keys:
                await self._page.keyboard.press(k)

    async def press_hotkey(self, *args: str) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        keys = "+".join(args)
        await self._page.keyboard.press(keys)

    async def move_to_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        validate_region(
            left,
            top,
            width,
            height,
            self._viewport_size["width"],
            self._viewport_size["height"],
        )
        if edge_sigma <= 0.0:
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = _get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )
        await self._page.mouse.move(x, y)

    async def scroll(self, clicks: int) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101

        if clicks == 0:
            return

        if clicks > 0:
            delta = 58 * 2
        else:
            logger.debug("scroll clicks is smaller than 0.")
            assert clicks < 0  # noqa: S101
            delta = -58 * 2
            clicks = abs(clicks)

        await self._page.mouse.wheel(delta_x=0, delta_y=delta)
        for _ in range(clicks - 1):
            await asyncio.sleep(0.1)
            await self._page.mouse.wheel(delta_x=0, delta_y=delta)

    async def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        validate_region(
            left,
            top,
            width,
            height,
            self._viewport_size["width"],
            self._viewport_size["height"],
        )
        if edge_sigma <= 0.0:
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = _get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )
        await self._page.mouse.click(x, y)

    async def get_screenshot(self) -> bytes:
        """Return bytes in png format."""
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        return await self._page.screenshot()

    async def close(self) -> None:
        self._assert_launched()
        assert self._context_manager is not None  # noqa: S101
        assert self._context is not None  # noqa: S101

        await self._context.close()
        if self._browser is not None:
            await self._browser.close()
        await self._context_manager.__aexit__()


class RemoteBrowser(BrowserBase):
    def __init__(
        self,
        remote_host: str,
        remote_port: int = 19222,
    ) -> None:
        super().__init__()
        ip_address(remote_host)
        validate_user_port(remote_port)

        self._context = zmq.asyncio.Context()  # type: ignore[attr-defined]
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(f"tcp://{remote_host}:{remote_port}")

    async def _communicate(self, request: object) -> dict[str, Any]:
        jsonized_request = json.dumps(request, separators=(",", ":"))
        encoded_request = jsonized_request.encode(encoding="utf-8")
        await self._socket.send(encoded_request)

        encoded_response = await self._socket.recv()
        jsonized_response = encoded_response.decode(encoding="utf-8")
        response = json.loads(jsonized_response)

        if not isinstance(response, dict):
            msg = "An invalid message was received."
            raise TypeError(msg)
        if any(not isinstance(key, str) for key in response):
            msg = "An invalid message was received."
            raise TypeError(msg)
        return response

    @staticmethod
    def _check_response(response: dict[str, object]) -> None:
        if response["result"] != "O.K.":
            msg = "Failed to send a message to the remote browser."
            raise RuntimeError(msg)

    async def get_zoom_ratio(self) -> float:
        request = {"type": "zoom_ratio"}
        response = await self._communicate(request)
        self._check_response(response)
        return response["data"]

    async def refresh(self) -> None:
        request = {"type": "refresh"}
        response = await self._communicate(request)
        self._check_response(response)

    async def write(self, text: str, delay: float | None = None) -> None:
        request = {"type": "write", "text": text, "delay": delay}
        response = await self._communicate(request)
        self._check_response(response)

    async def press(self, keys: str | Iterable[str]) -> None:
        if not isinstance(keys, str):
            keys = list(keys)
        request = {"type": "press", "keys": keys}
        response = await self._communicate(request)
        self._check_response(response)

    async def press_hotkey(self, *args: str) -> None:
        request = {"type": "press_hotkey", "args": list(args)}
        response = await self._communicate(request)
        self._check_response(response)

    async def move_to_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        viewport_size = await self._get_viewport_size()

        validate_region(
            left,
            top,
            width,
            height,
            viewport_size["width"],
            viewport_size["height"],
        )
        if edge_sigma <= 0.0:
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = _get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )

        request = {"type": "move", "x": x, "y": y}
        response = await self._communicate(request)
        self._check_response(response)

    async def scroll(self, clicks: int) -> None:
        request = {"type": "scroll", "clicks": clicks}
        response = await self._communicate(request)
        self._check_response(response)

    async def _get_viewport_size(self) -> dict[str, int]:
        request = {"type": "_get_viewport_size"}
        response = await self._communicate(request)
        self._check_response(response)
        return response["data"]

    async def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        viewport_size = await self._get_viewport_size()

        validate_region(
            left,
            top,
            width,
            height,
            viewport_size["width"],
            viewport_size["height"],
        )
        if edge_sigma <= 0.0:
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
        response = await self._communicate(request)
        self._check_response(response)

    async def get_screenshot(self) -> bytes:
        request = {"type": "get_screenshot"}
        response = await self._communicate(request)
        self._check_response(response)
        data: str = response["data"]
        return base64.b64decode(data)

    async def close(self) -> None:
        self._socket.close()
        self._context.destroy()
