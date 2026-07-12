import asyncio
from collections import deque
from dataclasses import dataclass

from majsoulrpa.sniffer.events import DecodedSnifferMessage, RawNotice


class SnifferHistoryGapError(RuntimeError):
    """Raised when a cursor points before the retained event history."""


class SnifferEventTooLargeError(RuntimeError):
    """Raised when one selected event exceeds the byte budget."""


@dataclass(frozen=True, slots=True)
class SnifferEventCursor:
    sequence: int


@dataclass(frozen=True, slots=True)
class _StoredEvent:
    sequence: int
    message: DecodedSnifferMessage
    payload_bytes: int


class SnifferEventStore:
    """Finite, non-destructive history of decoded Sniffer events."""

    def __init__(
        self,
        *,
        names: set[str],
        capacity: int,
        max_payload_bytes: int = 64 * 1024 * 1024,
    ) -> None:
        if capacity <= 0:
            msg = "Sniffer event store capacity must be positive."
            raise ValueError(msg)
        if max_payload_bytes <= 0:
            msg = "Sniffer event store max_payload_bytes must be positive."
            raise ValueError(msg)
        self._names = frozenset(names)
        self._capacity = capacity
        self._max_payload_bytes = max_payload_bytes
        self._events: deque[_StoredEvent] = deque()
        self._retained_payload_bytes = 0
        self._latest_sequence = 0
        self._evicted_through = 0
        self._changed = asyncio.Condition()

    def cursor(self) -> SnifferEventCursor:
        return SnifferEventCursor(self._latest_sequence)

    async def append(self, message: DecodedSnifferMessage) -> None:
        async with self._changed:
            self._latest_sequence += 1

            if message.raw.name not in self._names:
                return

            payload_bytes = _payload_size(message)
            if payload_bytes > self._max_payload_bytes:
                msg = "Sniffer event exceeds the store byte budget."
                raise SnifferEventTooLargeError(msg)

            while self._events and (
                len(self._events) >= self._capacity
                or self._retained_payload_bytes + payload_bytes
                > self._max_payload_bytes
            ):
                evicted = self._events.popleft()
                self._retained_payload_bytes -= evicted.payload_bytes
                self._evicted_through = evicted.sequence

            self._events.append(
                _StoredEvent(
                    self._latest_sequence,
                    message,
                    payload_bytes,
                ),
            )
            self._retained_payload_bytes += payload_bytes
            self._changed.notify_all()

    def messages_after(
        self,
        cursor: SnifferEventCursor,
    ) -> tuple[DecodedSnifferMessage, ...]:
        self._require_retained(cursor)
        return tuple(
            event.message
            for event in self._events
            if event.sequence > cursor.sequence
        )

    async def wait_for(
        self,
        name: str,
        *,
        after: SnifferEventCursor,
    ) -> DecodedSnifferMessage:
        async with self._changed:
            while True:
                self._require_retained(after)
                for event in tuple(self._events):
                    if (
                        event.sequence > after.sequence
                        and event.message.raw.name == name
                    ):
                        self._events.remove(event)
                        self._retained_payload_bytes -= event.payload_bytes
                        return event.message
                await self._changed.wait()

    def _require_retained(self, cursor: SnifferEventCursor) -> None:
        if cursor.sequence > self._latest_sequence:
            msg = "Sniffer event cursor is ahead of this store."
            raise ValueError(msg)
        if cursor.sequence < self._evicted_through:
            msg = "Sniffer event history no longer contains the cursor."
            raise SnifferHistoryGapError(msg)


def _payload_size(message: DecodedSnifferMessage) -> int:
    raw = message.raw
    if isinstance(raw, RawNotice):
        return len(raw.payload)
    return len(raw.request) + len(raw.response)
