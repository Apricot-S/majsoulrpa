import datetime
import uuid

import pytest

from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
)
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
        schema_version=1,
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


def test_mixed_stream_tracks_publication_sequence_only() -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(1))
    tracker.observe(
        RequestResponsePublication(
            schema_version=1,
            stream_id=STREAM_ID,
            publication_sequence=2,
            connection_id="connection-1",
            request_direction=Direction.OUTBOUND,
            request_number=0,
            request_frame_sequence=10,
            response_frame_sequence=12,
            request_observed_at=OBSERVED_AT,
            response_observed_at=OBSERVED_AT,
            api_name=".lq.SyntheticService.call",
            request_payload_base64="c3ludGhldGlj",
            response_payload_base64="c3ludGhldGlj",
        )
    )
    data = _publication(3).model_dump()
    data.update(connection_id="connection-2", frame_sequence=1)
    tracker.observe(NoticePublication.model_validate(data))

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == 3
    assert tracker.started_midstream is False

    data.update(publication_sequence=5, frame_sequence=2)
    with pytest.raises(
        PublicationSequenceGapError, match=r"expected 4.*received 5"
    ):
        tracker.observe(NoticePublication.model_validate(data))
    assert tracker.last_sequence == 3


@pytest.mark.parametrize(
    "first_sequence", [1, 4], ids=["from-start", "midstream"]
)
@pytest.mark.parametrize(
    "offset", [0, 1, 2], ids=["duplicate", "contiguous", "gap"]
)
def test_stream_id_change_is_rejected_without_replacing_state(
    first_sequence: int,
    offset: int,
) -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(first_sequence))

    with pytest.raises(PublicationStreamRestartError, match="stream_id"):
        tracker.observe(
            _publication(first_sequence + offset, stream_id=OTHER_STREAM_ID)
        )

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == first_sequence
    assert tracker.started_midstream is (first_sequence > 1)

    tracker.observe(_publication(first_sequence + 1))

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == first_sequence + 1
    assert tracker.started_midstream is (first_sequence > 1)


@pytest.mark.parametrize(
    "first_sequence", [1, 4], ids=["from-start", "midstream"]
)
def test_sequence_gap_is_rejected_without_advancing_state(
    first_sequence: int,
) -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(first_sequence))

    for sequence in (first_sequence + 2, first_sequence + 3):
        with pytest.raises(
            PublicationSequenceGapError,
            match=f"expected {first_sequence + 1}.*received {sequence}",
        ):
            tracker.observe(_publication(sequence))

        assert tracker.stream_id == STREAM_ID
        assert tracker.last_sequence == first_sequence
        assert tracker.started_midstream is (first_sequence > 1)

    tracker.observe(_publication(first_sequence + 1))
    tracker.observe(_publication(first_sequence + 2))

    assert tracker.last_sequence == first_sequence + 2
    assert tracker.started_midstream is (first_sequence > 1)


@pytest.mark.parametrize(
    "first_sequence", [1, 4], ids=["from-start", "midstream"]
)
@pytest.mark.parametrize("offset", [0, 1], ids=["rollback", "duplicate"])
def test_duplicate_or_rollback_is_rejected(
    first_sequence: int,
    offset: int,
) -> None:
    tracker = PublicationStreamTracker()
    tracker.observe(_publication(first_sequence))
    tracker.observe(_publication(first_sequence + 1))

    with pytest.raises(
        PublicationSequenceRollbackError, match=f"last {first_sequence + 1}"
    ):
        tracker.observe(_publication(first_sequence + offset))

    assert tracker.stream_id == STREAM_ID
    assert tracker.last_sequence == first_sequence + 1
    assert tracker.started_midstream is (first_sequence > 1)

    tracker.observe(_publication(first_sequence + 2))

    assert tracker.last_sequence == first_sequence + 2
    assert tracker.started_midstream is (first_sequence > 1)
