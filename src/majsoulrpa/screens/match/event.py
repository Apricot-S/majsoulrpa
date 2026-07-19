import datetime
from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, slots=True, kw_only=True)
class _MatchEventBase:
    action_step: int
    observed_at: datetime.datetime | None

    def __post_init__(self) -> None:
        if self.action_step < 0:
            msg = "action_step must be nonnegative."
            raise ValueError(msg)

        if self.observed_at is None:
            return
        if (
            self.observed_at.tzinfo is None
            or self.observed_at.utcoffset() is None
        ):
            msg = "observed_at must be timezone-aware."
            raise ValueError(msg)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class StartMatchEvent(_MatchEventBase):
    pass


type MatchEvent = StartMatchEvent


__all__ = ["MatchEvent", "StartMatchEvent"]
