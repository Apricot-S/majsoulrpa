from collections.abc import Callable, Mapping
from typing import Any, Protocol

from majsoulrpa.config import AppConfig
from majsoulrpa.types import Callback

type ScreenTypes = tuple[type[object], ...]


class ScreenDetector(Protocol):
    async def detect(self, screen_types: ScreenTypes) -> object | None: ...


class RPARuntime:
    def __init__(
        self,
        callbacks: Mapping[type[object], Callback[Any]],
        detector: ScreenDetector,
    ) -> None:
        self._callbacks = callbacks
        self._detector = detector

    async def run(self, config: AppConfig, data: Any) -> Any:  # noqa: ANN401
        _ = config
        current_data = data
        screen_types = tuple(self._callbacks)

        while True:
            screen = await self._detector.detect(screen_types)
            if screen is None:
                return current_data

            callback = self._callbacks.get(type(screen))
            if callback is None:
                continue

            current_data = await callback(screen, current_data)


type RuntimeFactory = Callable[
    [Mapping[type[object], Callback[Any]]],
    RPARuntime,
]
