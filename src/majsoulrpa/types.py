from collections.abc import Awaitable, Callable
from typing import Any

type Callback[ScreenT] = Callable[[ScreenT, Any], Awaitable[Any]]
