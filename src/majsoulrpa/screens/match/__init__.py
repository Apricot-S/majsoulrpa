from typing import TYPE_CHECKING

from majsoulrpa.screens.match.event import (
    ChiEvent,
    DaminggangEvent,
    DapaiEvent,
    LiqiSuccess,
    MatchEvent,
    NewRoundEvent,
    PengEvent,
    StartMatchEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation import (
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    LiqiOperation,
    MatchOperation,
    OperationCandidates,
    PengOperation,
)
from majsoulrpa.screens.match.state import (
    Angang,
    Chi,
    Daminggang,
    Dapai,
    Fulu,
    Jiagang,
    MatchOrigin,
    MatchPlayer,
    MatchRank,
    MatchState,
    Peng,
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
    "Angang",
    "Chi",
    "ChiEvent",
    "ChiOperation",
    "Daminggang",
    "DaminggangEvent",
    "DaminggangOperation",
    "Dapai",
    "DapaiEvent",
    "DapaiOperation",
    "Fulu",
    "Jiagang",
    "LiqiOperation",
    "LiqiSuccess",
    "MatchEvent",
    "MatchOperation",
    "MatchOrigin",
    "MatchPlayer",
    "MatchRank",
    "MatchScreen",
    "MatchState",
    "NewRoundEvent",
    "OperationCandidates",
    "Peng",
    "PengEvent",
    "PengOperation",
    "RoundState",
    "Seat",
    "StartMatchEvent",
    "Tile",
    "ZimoEvent",
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
