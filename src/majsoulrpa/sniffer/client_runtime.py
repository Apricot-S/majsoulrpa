import asyncio
from typing import Protocol

from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.publication import SnifferPublication


class SnifferSubscriber(Protocol):
    async def connect(self) -> None: ...
    async def receive(self) -> SnifferPublication: ...
    async def stop(self) -> None: ...


class SnifferDecoder(Protocol):
    def decode(
        self,
        publication: SnifferPublication,
    ) -> DecodedSnifferMessage: ...


class DecodedMessageQueue(Protocol):
    def enqueue(self, message: DecodedSnifferMessage) -> None: ...


class SnifferMessageObserver(Protocol):
    def observe(self, message: DecodedSnifferMessage) -> None: ...


class SnifferClientRuntime:
    def __init__(
        self,
        *,
        subscriber: SnifferSubscriber,
        decoder: SnifferDecoder,
        observer: SnifferMessageObserver,
        queue: DecodedMessageQueue,
    ) -> None:
        self._subscriber = subscriber
        self._decoder = decoder
        self._observer = observer
        self._queue = queue
        self._connected = asyncio.Event()

    async def wait_until_ready(self) -> None:
        await self._connected.wait()

    async def run(self) -> None:
        try:
            await self._subscriber.connect()
            self._connected.set()
            while True:
                publication = await self._subscriber.receive()
                message = self._decoder.decode(publication)
                self._observer.observe(message)
                self._queue.enqueue(message)
        finally:
            await self._subscriber.stop()
