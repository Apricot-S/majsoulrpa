import asyncio
from abc import abstractmethod
from collections.abc import Iterable
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, override

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    ViewportSize,
    async_playwright,
)

from majsoulrpa.client._validation import validate_user_port

from .base import (
    STD_HEIGHT,
    STD_WIDTH,
    URL_MAJSOUL_JP,
    BrowserBase,
    get_random_point_in_region,
    validate_region,
    validate_viewport_size,
)

if TYPE_CHECKING:
    from playwright.async_api._context_manager import PlaywrightContextManager

logger = getLogger(__name__)


class LocalBrowserBase(BrowserBase):
    @abstractmethod
    def __init__(
        self,
        proxy_port: int,
        initial_left: int,
        initial_top: int,
        width: int,
        height: int,
        *,
        headless: bool,
        user_data_dir: str | Path | None,
    ) -> None:
        pass

    @abstractmethod
    async def launch(self) -> None:
        pass

    @abstractmethod
    def is_launched(self) -> bool:
        pass


class LocalBrowser(LocalBrowserBase):
    @override
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

    @override
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

        await self._page.goto(URL_MAJSOUL_JP)

    @override
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

    @override
    async def get_zoom_ratio(self) -> float:
        return self._zoom_ratio

    @override
    async def refresh(self) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        await self._page.reload()

    @override
    async def write(self, text: str, delay: float | None = None) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        await self._page.keyboard.type(text, delay=delay)

    @override
    async def press(self, keys: str | Iterable[str]) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101

        if isinstance(keys, str):
            await self._page.keyboard.press(keys)
        else:
            for k in keys:
                await self._page.keyboard.press(k)

    @override
    async def press_hotkey(self, *args: str) -> None:
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        keys = "+".join(args)
        await self._page.keyboard.press(keys)

    @override
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

        x, y = get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )
        await self._page.mouse.move(x, y)

    @override
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

    @override
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

        x, y = get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )
        await self._page.mouse.click(x, y)

    @override
    async def get_screenshot(self) -> bytes:
        """Return bytes in png format."""
        self._assert_launched()
        assert self._page is not None  # noqa: S101
        return await self._page.screenshot()

    @override
    async def close(self) -> None:
        self._assert_launched()
        assert self._context_manager is not None  # noqa: S101
        assert self._context is not None  # noqa: S101

        await self._context.close()
        if self._browser is not None:
            await self._browser.close()
        await self._context_manager.__aexit__()
