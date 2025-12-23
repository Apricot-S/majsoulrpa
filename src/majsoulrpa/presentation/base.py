import asyncio
import time
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Iterable
from functools import wraps
from logging import getLogger
from typing import ClassVar, Concatenate, Self

from majsoulrpa import browser, sniffer
from majsoulrpa.presentation import template
from majsoulrpa.presentation.delay import get_random_delay
from majsoulrpa.presentation.exceptions import InvalidOperationError
from majsoulrpa.presentation.region import (
    DEFAULT_EDGE_SIGMA,
    Region,
    get_random_point_in_region,
)

logger = getLogger(__name__)

DEFAULT_CLICK_BASE_DELAY = 120  # milliseconds
DEFAULT_CLICK_DELAY_SIGMA = 0.2

DEFAULT_WAIT_INTERVAL = 0.5  # seconds


class Presentation(ABC):
    _templates: ClassVar[dict[str, template.MatcherBase]] = {}
    _regions: ClassVar[dict[str, Region]] = {}

    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls._templates = dict(cls._templates)
        cls._regions = dict(cls._regions)

    def __init__(
        self,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> None:
        self._driver = driver
        self._message_queue = message_queue

        self.__scale: float | None = None
        self.__is_presentation_finished = False
        self.__is_rpa_ended = False
        self.__is_browser_closed = False

    async def get_screenshot(self) -> bytes:
        if self._is_rpa_ended:
            msg = (
                "`get_screenshot` called after RPA session has already ended."
            )
            raise InvalidOperationError(msg, None)
        return await self._driver.get_screenshot()

    async def reload(self) -> None:
        if self._is_rpa_ended:
            msg = "`reload` called after RPA session has already ended."
            raise InvalidOperationError(msg, None)
        self.__is_presentation_finished = True
        await self._driver.reload()

    async def end_rpa(self, *, close_browser: bool) -> None:
        self.__is_rpa_ended = True
        if (not self.__is_browser_closed) and close_browser:
            self.__is_browser_closed = True
            await self._driver.quit()

    @property
    def _scale(self) -> float:
        if self.__scale is None:
            msg = "resolution scale has not been initialized."
            raise RuntimeError(msg)
        return self.__scale

    @property
    def _is_presentation_finished(self) -> bool:
        return self.__is_presentation_finished

    @property
    def _is_rpa_ended(self) -> bool:
        return self.__is_rpa_ended

    def _mark_finished(self) -> None:
        if self.__is_presentation_finished:
            msg = "presentation is already finished."
            raise RuntimeError(msg)
        self.__is_presentation_finished = True

    async def _init_resolution(self) -> None:
        resolution = await self._driver.get_resolution()
        self.__scale = resolution.scale

    async def _press_key(
        self,
        key: str | Iterable[str],
        base_delay: float = 130,
        delay_sigma: float = 0.2,
    ) -> None:
        d = get_random_delay(base_delay, delay_sigma)
        await self._driver.press_key(key, d)

    async def _type_key(
        self,
        text: str,
        base_delay: float = 150,
        delay_sigma: float = 0.2,
    ) -> None:
        d = get_random_delay(base_delay, delay_sigma)
        await self._driver.type_key(text, d)

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
        base_delay: float = DEFAULT_CLICK_BASE_DELAY,
        delay_sigma: float = DEFAULT_CLICK_DELAY_SIGMA,
    ) -> None:
        x, y = get_random_point_in_region(scaled_region, edge_sigma)
        d = get_random_delay(base_delay, delay_sigma)
        await self._driver.click_mouse(x, y, d)

    async def _click_region(
        self,
        region: Region,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = DEFAULT_CLICK_BASE_DELAY,
        delay_sigma: float = DEFAULT_CLICK_DELAY_SIGMA,
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
        interval: float = DEFAULT_WAIT_INTERVAL,
    ) -> None:
        while True:
            if await self._has_match(matcher):
                return
            await asyncio.sleep(interval)

    async def _wait_until_match_one_of(
        self,
        matchers: Iterable[template.MatcherBase],
        interval: float = DEFAULT_WAIT_INTERVAL,
    ) -> None:
        while True:
            if await self._has_match_one_of(matchers):
                return
            await asyncio.sleep(interval)

    async def _click_if_match(
        self,
        matcher: template.MatcherBase,
        edge_sigma: float = DEFAULT_EDGE_SIGMA,
        base_delay: float = DEFAULT_CLICK_BASE_DELAY,
        delay_sigma: float = DEFAULT_CLICK_DELAY_SIGMA,
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
        base_delay: float = DEFAULT_CLICK_BASE_DELAY,
        delay_sigma: float = DEFAULT_CLICK_DELAY_SIGMA,
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
        base_delay: float = DEFAULT_CLICK_BASE_DELAY,
        delay_sigma: float = DEFAULT_CLICK_DELAY_SIGMA,
        interval: float = DEFAULT_WAIT_INTERVAL,
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
        base_delay: float = DEFAULT_CLICK_BASE_DELAY,
        delay_sigma: float = DEFAULT_CLICK_DELAY_SIGMA,
        interval: float = DEFAULT_WAIT_INTERVAL,
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
    async def _detect(
        cls,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> Self | None:
        pass

    @abstractmethod
    async def _pre_dispatch(self) -> None:
        pass


type _RPAAPI[T: Presentation, **P, R] = Callable[
    Concatenate[T, P],
    Awaitable[R],
]


def require_active[T: Presentation, **P, R](
    method: _RPAAPI[T, P, R],
) -> _RPAAPI[T, P, R]:
    @wraps(method)
    async def _require_active(self: T, *args: P.args, **kwargs: P.kwargs) -> R:
        if self._is_rpa_ended:
            msg = f"`{method.__name__}` called after RPA session has already ended."  # noqa: E501
            raise InvalidOperationError(msg, None)

        if self._is_presentation_finished:
            msg = f"`{method.__name__}` called after presentation finished."
            ss = await self.get_screenshot()
            raise InvalidOperationError(msg, ss)

        return await method(self, *args, **kwargs)

    return _require_active


def log_api_call[T: Presentation, **P, R](
    method: _RPAAPI[T, P, R],
) -> _RPAAPI[T, P, R]:
    @wraps(method)
    async def _log_api_call(self: T, *args: P.args, **kwargs: P.kwargs) -> R:
        logger.info("`%s` called", method.__name__)
        start = time.perf_counter()

        ret = await method(self, *args, **kwargs)

        duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info("`%s` completed (%d ms)", method.__name__, duration_ms)

        return ret

    return _log_api_call


def rpa_api[T: Presentation, **P, R](
    method: _RPAAPI[T, P, R],
) -> _RPAAPI[T, P, R]:
    return require_active(log_api_call(method))
