import asyncio
import datetime

import pytest

from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    Direction,
    RawNotice,
    RawRequestResponse,
)
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


def _exchange() -> DecodedRequestResponse:
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    return DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=".lq.SyntheticService.call",
            request=b"req",
            response=b"reply",
            request_observed_at=observed_at,
            response_observed_at=observed_at,
        ),
        request={},
        response={},
    )


@pytest.mark.parametrize("insertion", ["enqueue", "put_back"])
def test_exchange_byte_limit_counts_both_payloads(insertion: str) -> None:
    message = _exchange()
    queue = SnifferMessageQueue(capacity=3, max_payload_bytes=7)
    insert = queue.enqueue if insertion == "enqueue" else queue.put_back
    with pytest.raises(SnifferMessageTooLargeError):
        insert(message)
    assert queue.get_nowait() is None

    queue = SnifferMessageQueue(capacity=3, max_payload_bytes=8)
    insert = queue.enqueue if insertion == "enqueue" else queue.put_back
    insert(message)
    assert queue.get_nowait() is message


def test_mixed_payload_budget_is_released_and_restored_on_put_back() -> None:
    async def exercise() -> None:
        notice = _notice(".lq.SyntheticNotice", 1)
        exchange = _exchange()
        queue = SnifferMessageQueue(
            capacity=3, max_payload_bytes=len(notice.raw.payload) + 8
        )
        queue.enqueue(notice)
        queue.enqueue(exchange)
        with pytest.raises(SnifferMessageQueueOverflowError):
            queue.enqueue(exchange)

        assert await queue.get() is notice
        assert await queue.get() is exchange
        queue.put_back(exchange)
        queue.enqueue(notice)
        with pytest.raises(SnifferMessageQueueOverflowError):
            queue.enqueue(exchange)
        assert queue.get_nowait() is exchange
        assert queue.get_nowait() is notice
        assert queue.get_nowait() is None

    asyncio.run(exercise())


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


@pytest.mark.parametrize(
    ("capacity", "max_payload_bytes"),
    [(1, 1024), (3, len(b"synthetic-1"))],
    ids=["count-limit", "byte-limit"],
)
@pytest.mark.parametrize("insertion", ["enqueue", "put_back"])
def test_overflow_preserves_messages_and_reusable_capacity(
    capacity: int,
    max_payload_bytes: int,
    insertion: str,
) -> None:
    queue = SnifferMessageQueue(
        capacity=capacity,
        max_payload_bytes=max_payload_bytes,
    )
    insert = queue.enqueue if insertion == "enqueue" else queue.put_back
    first = _notice(".lq.First", 1)
    second = _notice(".lq.Second", 2)
    insert(first)

    with pytest.raises(SnifferMessageQueueOverflowError):
        queue.enqueue(second)
    with pytest.raises(SnifferMessageQueueOverflowError):
        queue.put_back(second)

    assert queue.get_nowait() is first
    assert queue.get_nowait() is None

    insert(second)
    assert queue.get_nowait() is second
    assert queue.get_nowait() is None


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
