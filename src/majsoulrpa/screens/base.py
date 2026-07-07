import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from random import Random
from typing import Protocol

from majsoulrpa.constants import BASE_VIEWPORT_WIDTH, DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.presentation import Region

FILL_REGION_CLICK_TO_INPUT_DELAY_SECONDS = 0.5


class BrowserController(Protocol):
    async def click(self, x: float, y: float) -> object: ...
    async def input_text(self, text: str) -> object: ...
    async def press_key(self, key: str) -> object: ...
    async def screenshot(self) -> bytes: ...


class TemplateMatchResult(Protocol):
    region: Region


class TemplateMatcher(Protocol):
    def match(self, screenshot: object) -> TemplateMatchResult: ...
    def matches(self, screenshot: object) -> bool: ...


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

    async def click_region(self, region: Region) -> None:
        scaled_region = self.context.scale_region(region)
        await self._click_region(scaled_region)

    async def _click_region(self, scaled_region: Region) -> None:
        x, y = scaled_region.random_point(rng=self.context.rng)
        await self.context.browser.click(x, y)

    async def fill_region(
        self,
        region: Region,
        value: str,
        *,
        clear: bool = False,
    ) -> None:
        await self.click_region(region)
        await asyncio.sleep(FILL_REGION_CLICK_TO_INPUT_DELAY_SECONDS)
        if clear:
            await self.context.browser.press_key("ControlOrMeta+A")
            await asyncio.sleep(FILL_REGION_CLICK_TO_INPUT_DELAY_SECONDS)
            await self.context.browser.press_key("Backspace")
            await asyncio.sleep(FILL_REGION_CLICK_TO_INPUT_DELAY_SECONDS)
        await self.context.browser.input_text(value)

    async def matches(self, template: TemplateMatcher) -> bool:
        screenshot = await self.context.browser.screenshot()
        return template.matches(screenshot)

    async def click_if_match(self, template: TemplateMatcher) -> bool:
        screenshot = await self.context.browser.screenshot()
        if not template.matches(screenshot):
            return False

        result = template.match(screenshot)
        await self._click_region(result.region)
        return True

    @abstractmethod
    async def before_callback(self) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
