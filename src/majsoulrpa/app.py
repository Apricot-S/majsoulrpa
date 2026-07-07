import inspect
from collections.abc import Callable
from typing import Any

from majsoulrpa.client.controller_runtime import ControllerRuntimeFactory
from majsoulrpa.client.runtime import RPARuntime, RuntimeFactory
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen
from majsoulrpa.types import Callback


class RPAApp:
    def __init__(self, runtime_factory: RuntimeFactory | None = None) -> None:
        self._callbacks: dict[type[Screen], Callback[Any]] = {}
        self._runtime_factory = (
            runtime_factory or self._default_runtime_factory
        )

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
            config,
            data,
            detection_timeout=detection_timeout,
        )

    @staticmethod
    def _default_runtime_factory(
        callbacks: dict[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        return ControllerRuntimeFactory()(callbacks, config)
