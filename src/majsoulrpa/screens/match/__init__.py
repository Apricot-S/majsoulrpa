from typing import TYPE_CHECKING

from majsoulrpa.screens.match.event import (
    DapaiEvent,
    MatchEvent,
    NewRoundEvent,
    StartMatchEvent,
)
from majsoulrpa.screens.match.state import (
    MatchDapai,
    MatchFulu,
    MatchFuluKind,
    MatchOrigin,
    MatchPlayer,
    MatchRank,
    MatchState,
    RoundState,
)
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)

if TYPE_CHECKING:
    from majsoulrpa.screens.match.screen import MatchScreen

__all__ = [
    "DapaiEvent",
    "MatchDapai",
    "MatchEvent",
    "MatchFulu",
    "MatchFuluKind",
    "MatchOrigin",
    "MatchPlayer",
    "MatchRank",
    "MatchScreen",
    "MatchState",
    "NewRoundEvent",
    "RoundState",
    "Seat",
    "StartMatchEvent",
    "Tile",
    "validate_seat",
    "validate_tile",
]


def __getattr__(name: str) -> object:
    if name == "MatchScreen":
        from majsoulrpa.screens.match.screen import (  # noqa: PLC0415
            MatchScreen,
        )

        globals()[name] = MatchScreen
        return MatchScreen
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
