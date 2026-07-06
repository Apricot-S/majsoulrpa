from typing import Protocol

from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse


class BrowserCommandExecutor(Protocol):
    async def execute(self, command: BrowserCommand) -> BrowserResponse: ...


class BrowserRequestTransport(Protocol):
    async def recv_command(self) -> BrowserCommand: ...
    async def send_response(self, response: BrowserResponse) -> None: ...


class BrowserRequestHandler:
    def __init__(
        self,
        transport: BrowserRequestTransport,
        executor: BrowserCommandExecutor,
    ) -> None:
        self._transport = transport
        self._executor = executor

    async def handle_once(self) -> None:
        command = await self._transport.recv_command()
        response = await self._executor.execute(command)
        await self._transport.send_response(response)

    async def serve_forever(self) -> None:
        while True:
            await self.handle_once()
