import asyncio
import datetime

import pytest

from majsoulrpa.sniffer.event_store import (
    SnifferEventStore,
    SnifferEventTooLargeError,
    SnifferHistoryGapError,
)
from majsoulrpa.sniffer.events import DecodedNotice, Direction, RawNotice


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


def test_messages_after_cursor_can_be_read_repeatedly() -> None:
    async def exercise() -> None:
        store = SnifferEventStore(
            names={".lq.First", ".lq.Second"},
            capacity=3,
            max_payload_bytes=1024,
        )
        cursor = store.cursor()
        first = _notice(".lq.First", 1)
        second = _notice(".lq.Second", 2)

        await store.append(first)
        await store.append(second)

        assert store.messages_after(cursor) == (first, second)
        assert store.messages_after(cursor) == (first, second)

    asyncio.run(exercise())


def test_wait_for_name_ignores_matching_message_before_cursor() -> None:
    async def exercise() -> None:
        store = SnifferEventStore(
            names={".lq.Lobby.fetchGameRecord"},
            capacity=3,
            max_payload_bytes=1024,
        )
        old = _notice(".lq.Lobby.fetchGameRecord", 1)
        await store.append(old)
        cursor = store.cursor()
        other = _notice(".lq.Other", 2)
        expected = _notice(".lq.Lobby.fetchGameRecord", 3)

        async def publish() -> None:
            await asyncio.sleep(0)
            await store.append(other)
            await store.append(expected)

        publisher = asyncio.create_task(publish())
        actual = await store.wait_for(
            ".lq.Lobby.fetchGameRecord",
            after=cursor,
        )
        await publisher

        assert actual is expected
        assert store.messages_after(cursor) == ()

    asyncio.run(exercise())


def test_reading_from_evicted_cursor_raises_history_gap() -> None:
    async def exercise() -> None:
        store = SnifferEventStore(
            names={".lq.First", ".lq.Second", ".lq.Third"},
            capacity=2,
            max_payload_bytes=1024,
        )
        cursor = store.cursor()
        await store.append(_notice(".lq.First", 1))
        await store.append(_notice(".lq.Second", 2))
        await store.append(_notice(".lq.Third", 3))

        with pytest.raises(SnifferHistoryGapError):
            store.messages_after(cursor)
        with pytest.raises(SnifferHistoryGapError):
            await store.wait_for(".lq.Third", after=cursor)

    asyncio.run(exercise())


def test_event_store_rejects_non_positive_capacity() -> None:
    with pytest.raises(ValueError, match="capacity must be positive"):
        SnifferEventStore(names={".lq.First"}, capacity=0)


def test_event_store_keeps_only_selected_api_names() -> None:
    async def exercise() -> None:
        store = SnifferEventStore(
            names={".lq.Lobby.fetchGameRecord"},
            capacity=3,
            max_payload_bytes=1024,
        )
        cursor = store.cursor()

        await store.append(_notice(".lq.Unrelated", 1))

        assert store.messages_after(cursor) == ()

    asyncio.run(exercise())


def test_event_store_evicts_oldest_event_to_stay_within_byte_budget() -> None:
    async def exercise() -> None:
        store = SnifferEventStore(
            names={".lq.First", ".lq.Second"},
            capacity=3,
            max_payload_bytes=len(b"synthetic-1"),
        )
        cursor = store.cursor()

        await store.append(_notice(".lq.First", 1))
        await store.append(_notice(".lq.Second", 2))

        with pytest.raises(SnifferHistoryGapError):
            store.messages_after(cursor)

    asyncio.run(exercise())


def test_event_larger_than_byte_budget_is_rejected() -> None:
    async def exercise() -> None:
        store = SnifferEventStore(
            names={".lq.First"},
            capacity=3,
            max_payload_bytes=1,
        )

        with pytest.raises(SnifferEventTooLargeError):
            await store.append(_notice(".lq.First", 1))

    asyncio.run(exercise())
