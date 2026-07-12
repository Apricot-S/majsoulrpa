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


class SnifferClientRuntime:
    def __init__(
        self,
        *,
        subscriber: SnifferSubscriber,
        decoder: SnifferDecoder,
        queue: DecodedMessageQueue,
    ) -> None:
        self._subscriber = subscriber
        self._decoder = decoder
        self._queue = queue

    async def run(self) -> None:
        try:
            await self._subscriber.connect()
            while True:
                publication = await self._subscriber.receive()
                message = self._decoder.decode(publication)
                self._queue.enqueue(message)
        finally:
            await self._subscriber.stop()
