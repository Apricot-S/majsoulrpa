from zmq.asyncio import Socket

from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserResponse,
    dump_browser_command_json,
    dump_browser_response_json,
    parse_browser_command_json,
    parse_browser_response_json,
)


class BrowserZmqClientTransport:
    def __init__(self, socket: Socket) -> None:
        self._socket = socket

    async def send(self, command: BrowserCommand) -> None:
        await self._socket.send(dump_browser_command_json(command))

    async def recv(self) -> BrowserResponse:
        payload = await self._socket.recv()
        return parse_browser_response_json(payload)


class BrowserZmqServerTransport:
    def __init__(self, socket: Socket) -> None:
        self._socket = socket

    async def recv_command(self) -> BrowserCommand:
        payload = await self._socket.recv()
        return parse_browser_command_json(payload)

    async def send_response(self, response: BrowserResponse) -> None:
        await self._socket.send(dump_browser_response_json(response))
