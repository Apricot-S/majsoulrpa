import asyncio
from collections.abc import Callable, Mapping
from typing import Any, Protocol

from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen
from majsoulrpa.types import Callback

type ScreenTypes = tuple[type[Screen], ...]


class ScreenDetector(Protocol):
    async def detect(self, screen_types: ScreenTypes) -> Screen | None: ...


class RPARuntime:
    def __init__(
        self,
        callbacks: Mapping[type[Screen], Callback[Any]],
        detector: ScreenDetector,
    ) -> None:
        self._callbacks = callbacks
        self._detector = detector

    async def run(
        self,
        config: AppConfig,
        data: Any,  # noqa: ANN401
        *,
        detection_timeout: float | None = None,
    ) -> Any:  # noqa: ANN401
        _ = config
        current_data = data
        screen_types = tuple(self._callbacks)

        while True:
            screen = await self._detect(screen_types, detection_timeout)
            if screen is None:
                return current_data

            callback = self._callbacks.get(type(screen))
            if callback is None:
                continue

            current_data = await callback(screen, current_data)

    async def _detect(
        self,
        screen_types: ScreenTypes,
        detection_timeout: float | None,
    ) -> Screen | None:
        async with asyncio.timeout(detection_timeout):
            return await self._detector.detect(screen_types)


type RuntimeFactory = Callable[
    [Mapping[type[Screen], Callback[Any]]],
    RPARuntime,
]
