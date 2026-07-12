import asyncio
from collections import deque

from majsoulrpa.sniffer.events import DecodedSnifferMessage, RawNotice


class SnifferMessageQueueOverflowError(RuntimeError):
    """Raised when another unread message cannot be retained."""


class SnifferMessageTooLargeError(RuntimeError):
    """Raised when one message exceeds the queue byte budget."""


class SnifferMessageQueue:
    """Bounded queue of all decoded messages with explicit put-back."""

    def __init__(
        self,
        *,
        capacity: int,
        max_payload_bytes: int,
    ) -> None:
        if capacity <= 0:
            msg = "Sniffer message queue capacity must be positive."
            raise ValueError(msg)
        if max_payload_bytes <= 0:
            msg = "Sniffer message queue max_payload_bytes must be positive."
            raise ValueError(msg)
        self._capacity = capacity
        self._max_payload_bytes = max_payload_bytes
        self._messages: asyncio.Queue[DecodedSnifferMessage] = asyncio.Queue()
        self._put_back_messages: deque[DecodedSnifferMessage] = deque()
        self._retained_payload_bytes = 0

    async def get(self) -> DecodedSnifferMessage:
        if self._put_back_messages:
            message = self._put_back_messages.popleft()
        else:
            message = await self._messages.get()
        self._retained_payload_bytes -= _payload_size(message)
        return message

    def get_nowait(self) -> DecodedSnifferMessage | None:
        if self._put_back_messages:
            message = self._put_back_messages.popleft()
        elif self._messages.empty():
            return None
        else:
            message = self._messages.get_nowait()
        self._retained_payload_bytes -= _payload_size(message)
        return message

    def enqueue(self, message: DecodedSnifferMessage) -> None:
        self._retain(message)
        self._messages.put_nowait(message)

    def put_back(self, message: DecodedSnifferMessage) -> None:
        self._retain(message)
        self._put_back_messages.append(message)

    def _retain(self, message: DecodedSnifferMessage) -> None:
        payload_bytes = _payload_size(message)
        if payload_bytes > self._max_payload_bytes:
            msg = "Sniffer message exceeds the queue byte budget."
            raise SnifferMessageTooLargeError(msg)
        if (
            self._messages.qsize() + len(self._put_back_messages)
            >= self._capacity
            or self._retained_payload_bytes + payload_bytes
            > self._max_payload_bytes
        ):
            msg = "Sniffer message queue is full."
            raise SnifferMessageQueueOverflowError(msg)
        self._retained_payload_bytes += payload_bytes


def _payload_size(message: DecodedSnifferMessage) -> int:
    raw = message.raw
    if isinstance(raw, RawNotice):
        return len(raw.payload)
    return len(raw.request) + len(raw.response)
