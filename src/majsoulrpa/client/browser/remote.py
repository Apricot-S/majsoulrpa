import base64
import json
from abc import abstractmethod
from collections.abc import Iterable
from ipaddress import ip_address
from logging import getLogger
from typing import Any, Final, override

import zmq
import zmq.asyncio

from majsoulrpa.client._validation import validate_user_port

from .base import BrowserBase, get_random_point_in_region, validate_region

logger = getLogger(__name__)


MAX_LATENCY: Final[int] = 2_000  # ms


class RemoteBrowserBase(BrowserBase):
    @abstractmethod
    def __init__(self, remote_host: str, remote_port: int) -> None:
        pass


class RemoteBrowser(RemoteBrowserBase):
    @override
    def __init__(self, remote_host: str, remote_port: int = 19222) -> None:
        ip_address(remote_host)
        validate_user_port(remote_port)

        self._context = zmq.asyncio.Context()  # type: ignore[attr-defined]
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(f"tcp://{remote_host}:{remote_port}")

    async def _communicate(self, request: object) -> dict[str, Any]:
        jsonized_request = json.dumps(request, separators=(",", ":"))
        encoded_request = jsonized_request.encode(encoding="utf-8")
        await self._socket.send(encoded_request)

        encoded_response = await self._socket.recv()
        jsonized_response = encoded_response.decode(encoding="utf-8")
        response = json.loads(jsonized_response)

        if not isinstance(response, dict):
            msg = "An invalid message was received."
            raise TypeError(msg)
        if any(not isinstance(key, str) for key in response):
            msg = "An invalid message was received."
            raise TypeError(msg)
        return response

    @staticmethod
    def _check_response(response: dict[str, object]) -> None:
        if response["result"] != "O.K.":
            msg = "Failed to send a message to the remote browser."
            raise RuntimeError(msg)

    @override
    async def get_zoom_ratio(self) -> float:
        request = {"type": "zoom_ratio"}
        response = await self._communicate(request)
        self._check_response(response)
        return response["data"]

    @override
    async def refresh(self) -> None:
        request = {"type": "refresh"}
        response = await self._communicate(request)
        self._check_response(response)

    @override
    async def write(self, text: str, delay: float | None = None) -> None:
        request = {"type": "write", "text": text, "delay": delay}
        response = await self._communicate(request)
        self._check_response(response)

    @override
    async def press(self, keys: str | Iterable[str]) -> None:
        if not isinstance(keys, str):
            keys = list(keys)
        request = {"type": "press", "keys": keys}
        response = await self._communicate(request)
        self._check_response(response)

    @override
    async def press_hotkey(self, *args: str) -> None:
        request = {"type": "press_hotkey", "args": list(args)}
        response = await self._communicate(request)
        self._check_response(response)

    @override
    async def move_to_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        viewport_size = await self._get_viewport_size()

        validate_region(
            left,
            top,
            width,
            height,
            viewport_size["width"],
            viewport_size["height"],
        )
        if edge_sigma <= 0.0:
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )

        request = {"type": "move", "x": x, "y": y}
        response = await self._communicate(request)
        self._check_response(response)

    @override
    async def scroll(self, clicks: int) -> None:
        request = {"type": "scroll", "clicks": clicks}
        response = await self._communicate(request)
        self._check_response(response)

    async def _get_viewport_size(self) -> dict[str, int]:
        request = {"type": "_get_viewport_size"}
        response = await self._communicate(request)
        self._check_response(response)
        return response["data"]

    @override
    async def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        viewport_size = await self._get_viewport_size()

        validate_region(
            left,
            top,
            width,
            height,
            viewport_size["width"],
            viewport_size["height"],
        )
        if edge_sigma <= 0.0:
            msg = "Invalid edge sigma was input."
            raise ValueError(msg)

        x, y = get_random_point_in_region(
            left,
            top,
            width,
            height,
            edge_sigma=edge_sigma,
        )

        request = {"type": "click", "x": x, "y": y}
        response = await self._communicate(request)
        self._check_response(response)

    @override
    async def get_screenshot(self) -> bytes:
        request = {"type": "get_screenshot"}
        response = await self._communicate(request)
        self._check_response(response)
        data: str = response["data"]
        return base64.b64decode(data)

    @override
    async def close(self) -> None:
        self._socket.close()
        self._context.destroy()
