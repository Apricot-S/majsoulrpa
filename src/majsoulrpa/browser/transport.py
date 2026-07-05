from typing import Protocol

from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse


class BrowserTransport(Protocol):
    async def send(self, command: BrowserCommand) -> None: ...

    async def recv(self) -> BrowserResponse: ...
