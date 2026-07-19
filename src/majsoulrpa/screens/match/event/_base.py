from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class _MatchEventBase:
    action_step: int

    def __post_init__(self) -> None:
        if self.action_step < 0:
            msg = "action_step must be nonnegative."
            raise ValueError(msg)
