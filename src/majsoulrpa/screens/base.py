from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from random import Random
from typing import Protocol

from majsoulrpa.constants import BASE_VIEWPORT_WIDTH, DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.presentation import Region


class BrowserController(Protocol):
    async def click(self, x: float, y: float) -> object: ...
    async def input_text(self, text: str) -> object: ...


type StopRequester = Callable[[], Awaitable[None]]


async def _ignore_stop_request() -> None:
    pass


class ScreenContext:
    def __init__(
        self,
        browser: BrowserController,
        request_stop: StopRequester | None = None,
        viewport_width: int = BASE_VIEWPORT_WIDTH,
        viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
        rng: Random | None = None,
    ) -> None:
        self._browser = browser
        self._request_stop = request_stop or _ignore_stop_request
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height
        self._rng = rng

    async def request_stop(self) -> None:
        await self._request_stop()

    def scale_region(self, region: Region) -> Region:
        return region.scale_to_viewport(
            width=self._viewport_width,
            height=self._viewport_height,
        )

    @property
    def browser(self) -> BrowserController:
        return self._browser

    @property
    def rng(self) -> Random | None:
        return self._rng


def _never_matches(_screenshot: object) -> bool:
    return False


@dataclass(frozen=True)
class ScreenDetectionSpec:
    predicate: Callable[[object], bool] = field(default=_never_matches)

    def matches(self, screenshot: object) -> bool:
        return self.predicate(screenshot)


class Screen(ABC):
    def __init__(self, context: ScreenContext | None = None) -> None:
        self._context = context

    @property
    def context(self) -> ScreenContext:
        if self._context is None:
            msg = "ScreenContext is not configured."
            raise RuntimeError(msg)
        return self._context

    async def fill_region(self, region: Region, value: str) -> None:
        scaled_region = self.context.scale_region(region)
        x, y = scaled_region.random_point(rng=self.context.rng)
        await self.context.browser.click(x, y)
        await self.context.browser.input_text(value)

    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
