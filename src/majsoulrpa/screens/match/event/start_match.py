from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match.event._base import _MatchEventBase


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class StartMatchEvent(_MatchEventBase):
    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        if action_step != 0:
            msg = "ActionMJStart must be step 0."
            raise ValueError(msg)
        if data:
            msg = "ActionMJStart must not contain known fields."
            raise ValueError(msg)
        return cls(action_step=action_step)
