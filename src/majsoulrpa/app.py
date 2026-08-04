import inspect
from collections.abc import Callable, Mapping
from typing import Any

from majsoulrpa.client.runtime import RPARuntime, RuntimeFactory
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen
from majsoulrpa.types import Callback


def _default_runtime_factory(
    callbacks: Mapping[type[Screen], Callback[Any]],
    config: AppConfig,
) -> RPARuntime:
    from majsoulrpa.client.controller_runtime import (  # noqa: PLC0415
        ControllerRuntimeFactory,
    )

    return ControllerRuntimeFactory()(callbacks, config)


class RPAApp:
    def __init__(
        self,
        runtime_factory: RuntimeFactory = _default_runtime_factory,
    ) -> None:
        self._callbacks: dict[type[Screen], Callback[Any]] = {}
        self._runtime_factory = runtime_factory

    @property
    def registered_screen_types(self) -> tuple[type[Screen], ...]:
        return tuple(self._callbacks)

    def on[ScreenT: Screen](
        self,
        screen_type: type[ScreenT],
    ) -> Callable[[Callback[ScreenT]], Callback[ScreenT]]:
        def register(callback: Callback[ScreenT]) -> Callback[ScreenT]:
            if not inspect.iscoroutinefunction(callback):
                msg = "RPAApp callbacks must be async functions."
                raise TypeError(msg)
            if screen_type in self._callbacks:
                screen_name = screen_type.__name__
                msg = f"Callback for {screen_name} is already registered."
                raise ValueError(msg)

            self._callbacks[screen_type] = callback
            return callback

        return register

    async def run(
        self,
        config: AppConfig,
        data: Any,  # noqa: ANN401
        *,
        detection_timeout: float | None = None,
    ) -> Any:  # noqa: ANN401
        runtime = self._runtime_factory(self._callbacks, config)
        return await runtime.run(
            data,
            detection_timeout=detection_timeout,
        )
