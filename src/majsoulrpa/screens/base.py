from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


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
    ) -> None:
        self._record_browser_operation = record_browser_operation
        self._request_stop = request_stop or _ignore_stop_request

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


def _never_matches(_screenshot: object) -> bool:
    return False


@dataclass(frozen=True)
class ScreenDetectionSpec:
    predicate: Callable[[object], bool] = field(default=_never_matches)

    def matches(self, screenshot: object) -> bool:
        return self.predicate(screenshot)


class Screen(ABC):
    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
