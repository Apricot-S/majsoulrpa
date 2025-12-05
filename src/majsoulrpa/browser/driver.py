import base64
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from typing import Self, override

from majsoulrpa.browser import schemas
from majsoulrpa.browser.client import ClientBase


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
    async def get_resolution(self) -> Resolution:
        req = schemas.ResolutionRequest()
        res = await self._client.send(req)
        res = expect_response(res, schemas.ResolutionResponse)
        return Resolution(width=res.width, height=res.height, scale=res.scale)

    @override
    async def move_mouse(self, x: float, y: float) -> None:
        req = schemas.MoveMouseRequest(x=x, y=y)
        await self._client.send(req)

    @override
    async def click_mouse(self, x: float, y: float, delay: float) -> None:
        req = schemas.ClickMouseRequest(x=x, y=y, delay=delay)
        await self._client.send(req)

    @override
    async def press_key(self, key: str | Iterable[str], delay: float) -> None:
        keys = key if isinstance(key, str) else "+".join(key)
        req = schemas.PressKeyRequest(key=keys, delay=delay)
        await self._client.send(req)

    @override
    async def type_key(self, text: str, delay: float) -> None:
        req = schemas.TypeKeyRequest(text=text, delay=delay)
        await self._client.send(req)

    @override
    async def get_screenshot(self) -> bytes:
        req = schemas.ScreenshotRequest()
        res = await self._client.send(req)
        res = expect_response(res, schemas.ScreenshotResponse)
        return base64.b64decode(res.image)

    @override
    async def reload(self) -> None:
        req = schemas.ReloadRequest()
        await self._client.send(req)

    @override
    async def quit(self) -> None:
        req = schemas.QuitRequest()
        await self._client.send(req)
