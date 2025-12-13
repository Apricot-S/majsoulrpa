import base64
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import StrEnum
from logging import getLogger
from time import perf_counter
from typing import Literal, Self, override

from majsoulrpa.browser import schemas
from majsoulrpa.browser.client import ClientBase

logger = getLogger(__name__)


class Key(StrEnum):
    CONTROL_OR_META = "ControlOrMeta"
    SHIFT = "Shift"
    BACKSPACE = "Backspace"


@dataclass(frozen=True)
class Resolution:
    width: int
    height: int
    scale: float


class DriverBase(ABC):
    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        pass

    @abstractmethod
    async def get_resolution(self) -> Resolution:
        pass

    @abstractmethod
    async def move_mouse(self, x: float, y: float) -> None:
        pass

    @abstractmethod
    async def click_mouse(self, x: float, y: float, delay: float) -> None:
        pass

    @abstractmethod
    async def press_key(self, key: str | Iterable[str], delay: float) -> None:
        pass

    @abstractmethod
    async def type_key(self, text: str, delay: float) -> None:
        pass

    @abstractmethod
    async def get_screenshot(self) -> bytes:
        pass

    @abstractmethod
    async def goto_log(self, log_id: str) -> None:
        pass

    @abstractmethod
    async def reload(self) -> None:
        pass

    @abstractmethod
    async def quit(self) -> None:
        pass


def expect_response[T: schemas.Response](
    res: schemas.Response,
    expected_type: type[T],
) -> T:
    if not isinstance(res, expected_type):
        msg = f"expected {expected_type.__name__}, got {type(res).__name__}"
        raise TypeError(msg)
    return res


def _elapsed_ms(start: float) -> int:
    """Computes elapsed time in milliseconds since `start`.

    Args:
        start: The starting timestamp obtained from
            `time.perf_counter()`.

    Returns:
        Elapsed time in milliseconds since `start`.
    """
    return int((perf_counter() - start) * 1000)


@asynccontextmanager
async def log_operation(
    name: str,
    level: Literal["debug", "info"] = "debug",
) -> AsyncGenerator:
    """Logs an operation with timing.

    Logs a start message when entering, and on exit logs either success
    with elapsed milliseconds or failure with exception details.

    Args:
        name: Operation name used in messages.
        level: Log severity ("info" or "debug"). Defaults to "debug".
    """
    log = logger.info if level == "info" else logger.debug
    log("%s requested", name)
    start = perf_counter()

    try:
        yield
    except Exception:
        elapsed = _elapsed_ms(start)
        logger.exception("%s failed (%d ms)", name, elapsed)
        raise
    else:
        elapsed = _elapsed_ms(start)
        log("%s success (%d ms)", name, elapsed)


class Driver(DriverBase):
    def __init__(self, client: ClientBase) -> None:
        self._client = client

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        pass

    @override
    @log_operation("get_resolution")
    async def get_resolution(self) -> Resolution:
        req = schemas.ResolutionRequest()
        res = await self._client.send(req)
        res = expect_response(res, schemas.ResolutionResponse)
        return Resolution(width=res.width, height=res.height, scale=res.scale)

    @override
    @log_operation("move_mouse")
    async def move_mouse(self, x: float, y: float) -> None:
        req = schemas.MoveMouseRequest(x=x, y=y)
        await self._client.send(req)

    @override
    @log_operation("click_mouse")
    async def click_mouse(self, x: float, y: float, delay: float) -> None:
        req = schemas.ClickMouseRequest(x=x, y=y, delay=delay)
        await self._client.send(req)

    @override
    @log_operation("press_key")
    async def press_key(self, key: str | Iterable[str], delay: float) -> None:
        keys = key if isinstance(key, str) else "+".join(key)
        req = schemas.PressKeyRequest(key=keys, delay=delay)
        await self._client.send(req)

    @override
    @log_operation("type_key")
    async def type_key(self, text: str, delay: float) -> None:
        req = schemas.TypeKeyRequest(text=text, delay=delay)
        await self._client.send(req)

    @override
    @log_operation("get_screenshot")
    async def get_screenshot(self) -> bytes:
        req = schemas.ScreenshotRequest()
        res = await self._client.send(req)
        res = expect_response(res, schemas.ScreenshotResponse)
        return base64.b64decode(res.image)

    @override
    @log_operation("goto_log", level="info")
    async def goto_log(self, log_id: str) -> None:
        req = schemas.LogRequest(log_id=log_id)
        await self._client.send(req)

    @override
    @log_operation("reload", level="info")
    async def reload(self) -> None:
        req = schemas.ReloadRequest()
        await self._client.send(req)

    @override
    @log_operation("quit", level="info")
    async def quit(self) -> None:
        req = schemas.QuitRequest()
        await self._client.send(req)
