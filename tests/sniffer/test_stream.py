import datetime
import uuid

import pytest

from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.publication import NoticePublication
from majsoulrpa.sniffer.stream import (
    PublicationSequenceGapError,
    PublicationSequenceRollbackError,
    PublicationStreamRestartError,
    PublicationStreamTracker,
)

STREAM_ID = uuid.UUID("12345678-1234-5678-1234-567812345678")
OTHER_STREAM_ID = uuid.UUID("87654321-4321-8765-4321-876543218765")
OBSERVED_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)


def _publication(
    sequence: int,
    *,
    stream_id: uuid.UUID = STREAM_ID,
) -> NoticePublication:
    return NoticePublication(
        stream_id=stream_id,
        publication_sequence=sequence,
        connection_id="connection-1",
        direction=Direction.INBOUND,
        frame_sequence=sequence,
        observed_at=OBSERVED_AT,
        api_name=".lq.SyntheticNotice",
        payload_base64="c3ludGhldGlj",
    )


def test_first_sequence_one_starts_complete_stream() -> None:
    tracker = PublicationStreamTracker()

    tracker.observe(_publication(1))

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == 1
    assert tracker.started_midstream is False


def test_first_sequence_greater_than_one_records_midstream_start() -> None:
    tracker = PublicationStreamTracker()

    tracker.observe(_publication(4))

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == 4
    assert tracker.started_midstream is True


def test_contiguous_sequence_advances_stream() -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(1))

    tracker.observe(_publication(2))

    assert tracker.last_sequence == 2


def test_stream_id_change_is_rejected_without_replacing_state() -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(1))

    with pytest.raises(PublicationStreamRestartError, match="stream_id"):
        tracker.observe(_publication(1, stream_id=OTHER_STREAM_ID))

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == 1


def test_sequence_gap_is_rejected_without_advancing_state() -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(1))

    with pytest.raises(
        PublicationSequenceGapError,
        match=r"expected 2.*received 3",
    ):
        tracker.observe(_publication(3))

    assert tracker.last_sequence == 1


@pytest.mark.parametrize("sequence", [1, 2])
def test_duplicate_or_rollback_is_rejected(
    sequence: int,
) -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(1))
    tracker.observe(_publication(2))

    with pytest.raises(PublicationSequenceRollbackError, match="last 2"):
        tracker.observe(_publication(sequence))

    assert tracker.last_sequence == 2
