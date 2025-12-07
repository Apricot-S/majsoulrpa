import asyncio
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Self

from majsoulrpa import browser
from majsoulrpa.presentation import template
from majsoulrpa.presentation.delay import get_random_delay
from majsoulrpa.presentation.region import (
    DEFAULT_EDGE_SIGMA,
    Region,
    get_random_point_in_region,
)


class Presentation(ABC):
    def __init__(self, driver: browser.DriverBase) -> None:
        self.__scale: float | None = None
        self._is_rpa_ended = False
        self._driver = driver

    async def get_screenshot(self) -> bytes:
        return await self._driver.get_screenshot()

    async def end_rpa(self, *, close_browser: bool) -> None:
        self._is_rpa_ended = True
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

    async def __click_scaled_region(
        self,
        scaled_region: Region,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
    ) -> None:
        x, y = get_random_point_in_region(scaled_region, edge_sigma)
        d = get_random_delay(base_delay, delay_sigma)
        await self._driver.click_mouse(x, y, d)

    async def _click_region(
        self,
        region: Region,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
    ) -> None:
        scaled = region.scale(self._scale)
        await self.__click_scaled_region(
            scaled,
            edge_sigma,
            base_delay,
            delay_sigma,
        )

    async def _has_match(self, matcher: template.MatcherBase) -> bool:
        screen = await self.get_screenshot()
        region = matcher.match(screen, self._scale)
        return region is not None

    async def _has_match_one_of(
        self,
        matchers: Iterable[template.MatcherBase],
    ) -> bool:
        screen = await self.get_screenshot()
        for matcher in matchers:
            region = matcher.match(screen, self._scale)
            if region is not None:
                return True
        return False

    async def _wait_until_match(
        self,
        matcher: template.MatcherBase,
        interval: float = 0.5,
    ) -> None:
        while True:
            if await self._has_match(matcher):
                return
            await asyncio.sleep(interval)

    async def _wait_until_match_one_of(
        self,
        matchers: Iterable[template.MatcherBase],
        interval: float = 0.5,
    ) -> None:
        while True:
            if await self._has_match_one_of(matchers):
                return
            await asyncio.sleep(interval)

    async def _click_if_match(
        self,
        matcher: template.MatcherBase,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
    ) -> bool:
        screen = await self.get_screenshot()
        region = matcher.match(screen, self._scale)
        if region is None:
            return False

        await self.__click_scaled_region(
            region,
            edge_sigma,
            base_delay,
            delay_sigma,
        )
        return True

    async def _click_if_match_one_of(
        self,
        matchers: Iterable[template.MatcherBase],
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
    ) -> bool:
        screen = await self.get_screenshot()
        for matcher in matchers:
            region = matcher.match(screen, self._scale)
            if region is not None:
                await self.__click_scaled_region(
                    region,
                    edge_sigma,
                    base_delay,
                    delay_sigma,
                )
                return True
        return False

    async def _click_when_match(
        self,
        matcher: template.MatcherBase,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
        interval: float = 0.5,
    ) -> None:
        while True:
            screen = await self.get_screenshot()
            region = matcher.match(screen, self._scale)
            if region is None:
                await asyncio.sleep(interval)
                continue

            await self.__click_scaled_region(
                region,
                edge_sigma,
                base_delay,
                delay_sigma,
            )
            return

    async def _click_when_match_one_of(
        self,
        matchers: Iterable[template.MatcherBase],
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = 100,
        delay_sigma: float = 0.1,
        interval: float = 0.5,
    ) -> None:
        while True:
            screen = await self.get_screenshot()
            for matcher in matchers:
                region = matcher.match(screen, self._scale)
                if region is not None:
                    await self.__click_scaled_region(
                        region,
                        edge_sigma,
                        base_delay,
                        delay_sigma,
                    )
                    return
            await asyncio.sleep(interval)

    @classmethod
    @abstractmethod
    async def _detect(cls, driver: browser.DriverBase) -> Self | None:
        pass

    @abstractmethod
    async def _pre_dispatch(self) -> None:
        pass
