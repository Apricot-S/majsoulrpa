from pydantic import TypeAdapter
from zmq.asyncio import Socket

from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse

_COMMAND_ADAPTER = TypeAdapter(BrowserCommand)
_RESPONSE_ADAPTER = TypeAdapter(BrowserResponse)


class BrowserZmqClientTransport:
    def __init__(self, socket: Socket) -> None:
        self._socket = socket

    async def send(self, command: BrowserCommand) -> None:
        await self._socket.send(_COMMAND_ADAPTER.dump_json(command))

    async def recv(self) -> BrowserResponse:
        payload = await self._socket.recv()
        return _RESPONSE_ADAPTER.validate_json(payload)


class BrowserZmqServerTransport:
    def __init__(self, socket: Socket) -> None:
        self._socket = socket

    async def recv_command(self) -> BrowserCommand:
        payload = await self._socket.recv()
        return _COMMAND_ADAPTER.validate_json(payload)

    async def send_response(self, response: BrowserResponse) -> None:
        await self._socket.send(_RESPONSE_ADAPTER.dump_json(response))
