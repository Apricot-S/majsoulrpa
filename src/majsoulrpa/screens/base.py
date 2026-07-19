import asyncio
import json
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Collection, Coroutine
from contextvars import ContextVar
from dataclasses import dataclass, field
from functools import wraps
from logging import getLogger
from random import Random
from typing import Concatenate, Protocol

from majsoulrpa.constants import BASE_VIEWPORT_WIDTH, DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.presentation import Region
from majsoulrpa.screens.errors import ScreenDetectionError, ScreenStaleError
from majsoulrpa.sniffer.events import DecodedNotice, DecodedSnifferMessage

SCREEN_ACTION_INTERVAL_SECONDS = 0.5
TEMPLATE_DETECTION_RETRY_INTERVAL_SECONDS = 0.5
LOG_URL_PREFIX = "https://game.mahjongsoul.com/?paipu="

_screen_api_logger = getLogger("majsoulrpa.screens.api")
_screen_api_depth: ContextVar[int] = ContextVar(
    "majsoulrpa_screen_api_depth",
    default=0,
)


class BrowserController(Protocol):
    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> object: ...
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
    @property
    def region(self) -> Region: ...


class TemplateMatcher(Protocol):
    def match(self, screenshot: object) -> TemplateMatchResult: ...
    def find(self, screenshot: object) -> TemplateMatchResult | None: ...
    def matches(self, screenshot: object) -> bool: ...


class SnifferMessageSource(Protocol):
    async def get(self) -> DecodedSnifferMessage: ...
    def get_nowait(self) -> DecodedSnifferMessage | None: ...
    def put_back(self, message: DecodedSnifferMessage) -> None: ...


class AccountState(Protocol):
    @property
    def account_id(self) -> int | None: ...


class _EmptyAccountState:
    @property
    def account_id(self) -> int | None:
        return None


_EMPTY_ACCOUNT_STATE = _EmptyAccountState()


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
        depth = _screen_api_depth.get()
        token = _screen_api_depth.set(depth + 1)
        try:
            if depth == 0:
                _screen_api_logger.info(
                    "screen API called: screen=%s api=%s",
                    type(self).__name__,
                    api_name,
                )
            return await method(self, *args, **kwargs)
        finally:
            _screen_api_depth.reset(token)

    return wrapper


async def _ignore_stop_request() -> None:
    pass


def _format_sniffer_message(message: DecodedSnifferMessage) -> str:
    if isinstance(message, DecodedNotice):
        value = {
            "raw": {
                "direction": message.raw.direction,
                "name": message.raw.name,
                "observed_at": message.raw.observed_at.isoformat(),
            },
            "message": message.message,
        }
    else:
        value = {
            "raw": {
                "request_direction": message.raw.request_direction,
                "name": message.raw.name,
                "request_observed_at": (
                    message.raw.request_observed_at.isoformat()
                ),
                "response_observed_at": (
                    message.raw.response_observed_at.isoformat()
                ),
            },
            "request": message.request,
            "response": message.response,
        }
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


class ScreenContext:
    def __init__(
        self,
        browser: BrowserController,
        sniffer_messages: SnifferMessageSource,
        request_stop: StopRequester | None = None,
        viewport_width: int = BASE_VIEWPORT_WIDTH,
        viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
        rng: Random | None = None,
        account_state: AccountState = _EMPTY_ACCOUNT_STATE,
    ) -> None:
        self._browser = browser
        self._sniffer_messages = sniffer_messages
        self._request_stop = request_stop or _ignore_stop_request
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height
        self._rng = rng
        self._account_state = account_state

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
    def sniffer_messages(self) -> SnifferMessageSource:
        return self._sniffer_messages

    @property
    def rng(self) -> Random | None:
        return self._rng

    @property
    def account_id(self) -> int | None:
        return self._account_state.account_id

    @property
    def viewport_height(self) -> int:
        return self._viewport_height


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

    async def _get_sniffer_message(self) -> DecodedSnifferMessage:
        await self._ensure_active()
        return await self.context.sniffer_messages.get()

    def _get_sniffer_message_nowait(self) -> DecodedSnifferMessage | None:
        return self.context.sniffer_messages.get_nowait()

    def _put_back_sniffer_message(
        self,
        message: DecodedSnifferMessage,
    ) -> None:
        self.context.sniffer_messages.put_back(message)

    async def _wait_for_sniffer_message(
        self,
        names: Collection[str],
        *,
        put_back_messages: bool = False,
    ) -> DecodedSnifferMessage:
        selected_names = frozenset(names)
        if not selected_names:
            msg = "Sniffer message names must not be empty."
            raise ValueError(msg)

        messages_to_put_back: list[DecodedSnifferMessage] = []
        try:
            while True:
                message = await self._get_sniffer_message()
                if put_back_messages:
                    messages_to_put_back.append(message)
                if message.raw.name in selected_names:
                    return message
        finally:
            for message in messages_to_put_back:
                self._put_back_sniffer_message(message)

    @property
    def context(self) -> ScreenContext:
        if self._context is None:
            msg = "ScreenContext is not configured."
            raise RuntimeError(msg)
        return self._context

    @_requires_active
    async def click_region(
        self,
        region: Region,
        *,
        warp: bool = False,
    ) -> None:
        scaled_region = self.context.scale_region(region)
        await self._click_region(scaled_region, warp=warp)

    async def _click_region(
        self,
        scaled_region: Region,
        *,
        warp: bool = False,
    ) -> None:
        x, y = scaled_region.random_point(rng=self.context.rng)
        await self.context.browser.click(x, y, warp=warp)

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

    @_requires_active
    async def wait_and_click_template(
        self,
        template: TemplateMatcher,
    ) -> TemplateMatchResult:
        while True:
            screenshot = await self.context.browser.screenshot()
            result = template.find(screenshot)
            if result is not None:
                await self._click_region(result.region)
                return result
            await asyncio.sleep(TEMPLATE_DETECTION_RETRY_INTERVAL_SECONDS)

    @_screen_api
    @_requires_active
    async def screenshot(self) -> bytes:
        return await self.context.browser.screenshot()

    @_screen_api
    @_requires_active
    async def reload(self) -> None:
        await self.context.browser.reload()
        self._mark_stale()

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
