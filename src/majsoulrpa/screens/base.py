from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from majsoulrpa.presentation import Region


@dataclass(frozen=True)
class BrowserOperation:
    name: str
    parameters: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        copied_parameters = dict(self.parameters)
        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(copied_parameters),
        )


type BrowserOperationRecorder = Callable[[BrowserOperation], Awaitable[None]]
type StopRequester = Callable[[], Awaitable[None]]


async def _ignore_stop_request() -> None:
    pass


class ScreenContext:
    def __init__(
        self,
        record_browser_operation: BrowserOperationRecorder,
        request_stop: StopRequester | None = None,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
    ) -> None:
        self._record_browser_operation = record_browser_operation
        self._request_stop = request_stop or _ignore_stop_request
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height

    async def record_browser_operation(
        self,
        name: str,
        **parameters: object,
    ) -> None:
        await self._record_browser_operation(
            BrowserOperation(name=name, parameters=parameters),
        )

    async def request_stop(self) -> None:
        await self._request_stop()

    def scale_region(self, region: Region) -> Region:
        return region.scale_to_viewport(
            width=self._viewport_width,
            height=self._viewport_height,
        )


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
        await self.context.record_browser_operation(
            "fill_region",
            region=self.context.scale_region(region),
            value=value,
        )

    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
