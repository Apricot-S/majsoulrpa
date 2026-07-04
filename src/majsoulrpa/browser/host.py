import asyncio
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
        try:
            await self._backend.start(config)
        except asyncio.CancelledError as cancellation:
            try:
                await self._backend.stop()
            except Exception as cleanup_error:
                self._running = False
                msg = "Browser host start was cancelled and cleanup failed."
                raise BaseExceptionGroup(
                    msg,
                    [cancellation, cleanup_error],
                ) from cleanup_error
            self._running = False
            raise
        else:
            self._running = True

    async def stop(self) -> None:
        if not self._running:
            return

        await self._backend.stop()
        self._running = False
