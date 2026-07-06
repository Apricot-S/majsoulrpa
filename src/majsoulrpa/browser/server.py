from typing import Protocol

from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse
from majsoulrpa.browser.transport import BrowserServerTransport


class BrowserCommandExecutor(Protocol):
    async def execute(self, command: BrowserCommand) -> BrowserResponse: ...


class BrowserRequestHandler:
    def __init__(
        self,
        transport: BrowserServerTransport,
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
