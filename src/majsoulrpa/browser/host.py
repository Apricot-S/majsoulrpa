from typing import Protocol

from majsoulrpa.config import AppConfig


class BrowserBackend(Protocol):
    async def start(self, config: AppConfig) -> None: ...

    async def stop(self) -> None: ...


class BrowserHost:
    def __init__(self, backend: BrowserBackend) -> None:
        self._backend = backend
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    async def start(self, config: AppConfig) -> None:
        await self._backend.start(config)
        self._running = True

    async def stop(self) -> None:
        if not self._running:
            return

        await self._backend.stop()
        self._running = False
