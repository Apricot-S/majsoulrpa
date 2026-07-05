import inspect
from collections.abc import Awaitable, Callable
from typing import Any

type Callback[ScreenT] = Callable[[ScreenT, Any], Awaitable[Any]]


class RPAApp:
    def __init__(self) -> None:
        self._callbacks: dict[type[object], Callback[Any]] = {}

    @property
    def registered_screen_types(self) -> tuple[type[object], ...]:
        return tuple(self._callbacks)

    def on[ScreenT](
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
