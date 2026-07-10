import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Coroutine
from contextvars import ContextVar
from dataclasses import dataclass, field
from functools import wraps
from logging import getLogger
from random import Random
from typing import Concatenate, Protocol

from majsoulrpa.constants import BASE_VIEWPORT_WIDTH, DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.presentation import Region
from majsoulrpa.screens.errors import ScreenDetectionError, ScreenStaleError

SCREEN_ACTION_INTERVAL_SECONDS = 0.5
LOG_URL_PREFIX = "https://game.mahjongsoul.com/?paipu="

SCREEN_API_LOGGER = getLogger("majsoulrpa.screens.api")
_SCREEN_API_DEPTH: ContextVar[int] = ContextVar(
    "majsoulrpa_screen_api_depth",
    default=0,
)


class BrowserController(Protocol):
    async def click(self, x: float, y: float) -> object: ...
    async def move_mouse(self, x: float, y: float) -> object: ...
    async def goto_url(self, url: str) -> object: ...
    async def reload(self) -> object: ...
    async def stop_browser_host(self) -> object: ...
    async def click_and_wait_for_yostar_auth(
        self,
        x: float,
        y: float,
    ) -> object: ...
    async def input_text(self, text: str) -> object: ...
    async def press_key(self, key: str) -> object: ...
    async def screenshot(self) -> bytes: ...


class TemplateMatchResult(Protocol):
    region: Region


class TemplateMatcher(Protocol):
    def match(self, screenshot: object) -> TemplateMatchResult: ...
    def find(self, screenshot: object) -> TemplateMatchResult | None: ...
    def matches(self, screenshot: object) -> bool: ...


type StopRequester = Callable[[], Awaitable[None]]


class _StaleAware(Protocol):
    async def _ensure_active(self) -> None: ...


def _requires_active[S: _StaleAware, R, **P](
    method: Callable[Concatenate[S, P], Coroutine[object, object, R]],
) -> Callable[Concatenate[S, P], Coroutine[object, object, R]]:
    @wraps(method)
    async def wrapper(self: S, *args: P.args, **kwargs: P.kwargs) -> R:
        await self._ensure_active()
        return await method(self, *args, **kwargs)

    return wrapper


def _screen_api[S, R, **P](
    method: Callable[Concatenate[S, P], Coroutine[object, object, R]],
) -> Callable[Concatenate[S, P], Coroutine[object, object, R]]:
    api_name = getattr(method, "__name__", type(method).__name__)

    @wraps(method)
    async def wrapper(self: S, *args: P.args, **kwargs: P.kwargs) -> R:
        depth = _SCREEN_API_DEPTH.get()
        token = _SCREEN_API_DEPTH.set(depth + 1)
        try:
            if depth == 0:
                SCREEN_API_LOGGER.info(
                    "screen API called: screen=%s api=%s",
                    type(self).__name__,
                    api_name,
                )
            return await method(self, *args, **kwargs)
        finally:
            _SCREEN_API_DEPTH.reset(token)

    return wrapper


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
        self._stale = False

    def _mark_stale(self) -> None:
        self._stale = True

    async def _ensure_active(self) -> None:
        if not self._stale:
            return
        screenshot = await self.context.browser.screenshot()
        msg = f"{type(self).__name__} is stale."
        raise ScreenStaleError(msg, screenshot)

    @property
    def context(self) -> ScreenContext:
        if self._context is None:
            msg = "ScreenContext is not configured."
            raise RuntimeError(msg)
        return self._context

    @_requires_active
    async def click_region(self, region: Region) -> None:
        scaled_region = self.context.scale_region(region)
        await self._click_region(scaled_region)

    async def _click_region(self, scaled_region: Region) -> None:
        x, y = scaled_region.random_point(rng=self.context.rng)
        await self.context.browser.click(x, y)

    @_requires_active
    async def move_region(self, region: Region) -> None:
        scaled_region = self.context.scale_region(region)
        x, y = scaled_region.random_point(rng=self.context.rng)
        await self.context.browser.move_mouse(x, y)

    @_requires_active
    async def fill_region(
        self,
        region: Region,
        value: str,
        *,
        clear: bool = False,
    ) -> None:
        await self.click_region(region)
        await asyncio.sleep(SCREEN_ACTION_INTERVAL_SECONDS)
        if clear:
            await self.context.browser.press_key("ControlOrMeta+A")
            await asyncio.sleep(SCREEN_ACTION_INTERVAL_SECONDS)
            await self.context.browser.press_key("Backspace")
            await asyncio.sleep(SCREEN_ACTION_INTERVAL_SECONDS)
        await self.context.browser.input_text(value)

    @_requires_active
    async def find_template(
        self,
        template: TemplateMatcher,
    ) -> TemplateMatchResult | None:
        screenshot = await self.context.browser.screenshot()
        return template.find(screenshot)

    @_requires_active
    async def require_template(
        self,
        template: TemplateMatcher,
        *,
        message: str,
    ) -> TemplateMatchResult:
        screenshot = await self.context.browser.screenshot()
        result = template.find(screenshot)
        if result is None:
            raise ScreenDetectionError(message, screenshot)
        return result

    @_requires_active
    async def click_template(
        self,
        template: TemplateMatcher,
        *,
        message: str,
    ) -> TemplateMatchResult:
        result = await self.require_template(template, message=message)
        await self._click_region(result.region)
        return result

    @_requires_active
    async def click_template_if_present(
        self,
        template: TemplateMatcher,
    ) -> bool:
        result = await self.find_template(template)
        if result is None:
            return False

        await self._click_region(result.region)
        return True

    @_screen_api
    @_requires_active
    async def screenshot(self) -> bytes:
        return await self.context.browser.screenshot()

    @_screen_api
    @_requires_active
    async def reload(self) -> None:
        await self.context.browser.reload()

    @_screen_api
    @_requires_active
    async def goto_log(self, log_id: str) -> None:
        await self.context.browser.goto_url(f"{LOG_URL_PREFIX}{log_id}")

    @_screen_api
    @_requires_active
    async def stop_browser_host(self) -> None:
        await self.context.browser.stop_browser_host()

    @_screen_api
    @_requires_active
    async def stop_rpa(self) -> None:
        await self.context.request_stop()

    @abstractmethod
    async def before_callback(self) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
