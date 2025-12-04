from abc import ABC, abstractmethod
from enum import StrEnum, auto

from majsoulrpa import browser
from majsoulrpa.presentation.delay import get_random_delay
from majsoulrpa.presentation.region import (
    DEFAULT_EDGE_SIGMA,
    Region,
    get_random_point_in_region,
)


class PresentationType(StrEnum):
    LOGIN = auto()


class Presentation(ABC):
    def __init__(self, driver: browser.DriverBase) -> None:
        self.__scale: float | None = None
        self._is_ended = False
        self._driver = driver

    async def get_screenshot(self) -> bytes:
        return await self._driver.get_screenshot()

    async def end(self, *, close_browser: bool) -> None:
        self._is_ended = True
        if close_browser:
            await self._driver.quit()

    @property
    def _scale(self) -> float:
        if self.__scale is None:
            msg = "resolution scale has not been initialized."
            raise RuntimeError(msg)
        return self.__scale

    async def _init_resolution(self) -> None:
        resolution = await self._driver.get_resolution()
        self.__scale = resolution.scale

    async def _move_to_region(
        self,
        region: Region,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
    ) -> None:
        scaled = region.scale(self._scale)
        x, y = get_random_point_in_region(scaled, edge_sigma)
        await self._driver.move_mouse(x, y)

    async def _click_region(
        self,
        region: Region,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
    ) -> None:
        scaled = region.scale(self._scale)
        x, y = get_random_point_in_region(scaled, edge_sigma)
        d = get_random_delay(base_delay, delay_sigma)
        await self._driver.click_mouse(x, y, d)

    @staticmethod
    @abstractmethod
    def get_type() -> PresentationType:
        pass

    @classmethod
    @abstractmethod
    async def _detect(cls, driver: browser.DriverBase) -> bool:
        pass

    @abstractmethod
    async def _pre_dispatch(self) -> None:
        pass
