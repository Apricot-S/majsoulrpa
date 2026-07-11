import uuid

from majsoulrpa.sniffer.publication import SnifferPublication


class PublicationStreamError(RuntimeError):
    """Base class for publication stream continuity failures."""


class PublicationStreamRestartError(PublicationStreamError):
    """Raised when a subscriber observes a different stream ID."""


class PublicationSequenceGapError(PublicationStreamError):
    """Raised when one or more publications are missing."""


class PublicationSequenceRollbackError(PublicationStreamError):
    """Raised when a sequence is duplicated or moves backwards."""


class PublicationStreamTracker:
    def __init__(self) -> None:
        self._stream_id: uuid.UUID | None = None
        self._last_sequence: int | None = None
        self._started_midstream: bool | None = None

    @property
    def stream_id(self) -> uuid.UUID | None:
        return self._stream_id

    @property
    def last_sequence(self) -> int | None:
        return self._last_sequence

    @property
    def started_midstream(self) -> bool | None:
        return self._started_midstream

    def observe(self, publication: SnifferPublication) -> None:
        if self._stream_id is None:
            self._stream_id = publication.stream_id
            self._last_sequence = publication.publication_sequence
            self._started_midstream = publication.publication_sequence > 1
            return

        if publication.stream_id != self._stream_id:
            msg = "Publication stream_id changed while subscribing."
            raise PublicationStreamRestartError(msg)

        last_sequence = self._last_sequence
        if last_sequence is None:
            msg = "Publication stream tracker has no last sequence."
            raise RuntimeError(msg)

        sequence = publication.publication_sequence
        if sequence <= last_sequence:
            msg = (
                "Publication sequence was duplicated or rolled back: "
                f"last {last_sequence}, received {sequence}."
            )
            raise PublicationSequenceRollbackError(msg)

        expected = last_sequence + 1
        if sequence != expected:
            msg = (
                "Publication sequence has a gap: "
                f"expected {expected}, received {sequence}."
            )
            raise PublicationSequenceGapError(msg)

        self._last_sequence = sequence
