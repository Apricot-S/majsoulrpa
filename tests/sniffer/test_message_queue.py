import asyncio
import datetime

import pytest

from majsoulrpa.sniffer.events import DecodedNotice, Direction, RawNotice
from majsoulrpa.sniffer.message_queue import (
    SnifferMessageQueue,
    SnifferMessageQueueOverflowError,
    SnifferMessageTooLargeError,
)


def _notice(name: str, second: int) -> DecodedNotice:
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=name,
            payload=f"synthetic-{second}".encode(),
            observed_at=datetime.datetime(
                2026,
                1,
                2,
                3,
                4,
                second,
                tzinfo=datetime.UTC,
            ),
        ),
        message={},
    )


def _queue(*, capacity: int = 3) -> SnifferMessageQueue:
    return SnifferMessageQueue(
        capacity=capacity,
        max_payload_bytes=1024,
    )


def test_queue_retains_all_messages_in_arrival_order() -> None:
    async def exercise() -> None:
        queue = _queue()
        first = _notice(".lq.First", 1)
        second = _notice(".lq.Second", 2)

        queue.enqueue(first)
        queue.enqueue(second)

        assert await queue.get() is first
        assert await queue.get() is second
        assert queue.get_nowait() is None

    asyncio.run(exercise())


def test_get_waits_for_next_message() -> None:
    async def exercise() -> None:
        queue = _queue()
        expected = _notice(".lq.First", 1)

        async def publish() -> None:
            await asyncio.sleep(0)
            queue.enqueue(expected)

        publisher = asyncio.create_task(publish())
        assert await queue.get() is expected
        await publisher

    asyncio.run(exercise())


def test_put_back_messages_are_read_before_unread_messages() -> None:
    async def exercise() -> None:
        queue = _queue()
        first = _notice(".lq.First", 1)
        second = _notice(".lq.Second", 2)
        queue.enqueue(first)
        queue.enqueue(second)

        consumed = await queue.get()
        queue.put_back(consumed)

        assert await queue.get() is first
        assert await queue.get() is second

    asyncio.run(exercise())


def test_multiple_put_back_messages_keep_put_back_order() -> None:
    async def exercise() -> None:
        queue = _queue()
        first = _notice(".lq.First", 1)
        second = _notice(".lq.Second", 2)

        queue.put_back(first)
        queue.put_back(second)

        assert await queue.get() is first
        assert await queue.get() is second

    asyncio.run(exercise())


def test_queue_overflow_is_not_silently_dropped() -> None:
    queue = _queue(capacity=1)
    queue.enqueue(_notice(".lq.First", 1))

    with pytest.raises(SnifferMessageQueueOverflowError):
        queue.enqueue(_notice(".lq.Second", 2))


def test_byte_budget_overflow_is_not_silently_dropped() -> None:
    queue = SnifferMessageQueue(
        capacity=3,
        max_payload_bytes=len(b"synthetic-1"),
    )
    queue.enqueue(_notice(".lq.First", 1))

    with pytest.raises(SnifferMessageQueueOverflowError):
        queue.enqueue(_notice(".lq.Second", 2))


def test_message_larger_than_byte_budget_is_rejected() -> None:
    queue = SnifferMessageQueue(capacity=3, max_payload_bytes=1)

    with pytest.raises(SnifferMessageTooLargeError):
        queue.enqueue(_notice(".lq.First", 1))


@pytest.mark.parametrize(
    ("capacity", "max_payload_bytes", "message"),
    [
        (0, 1, "capacity must be positive"),
        (1, 0, "max_payload_bytes must be positive"),
    ],
)
def test_queue_rejects_non_positive_limits(
    capacity: int,
    max_payload_bytes: int,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        SnifferMessageQueue(
            capacity=capacity,
            max_payload_bytes=max_payload_bytes,
        )
