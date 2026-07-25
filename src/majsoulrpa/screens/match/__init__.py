from typing import TYPE_CHECKING

from majsoulrpa.screens.match.event import (
    AngangEvent,
    BabeiEvent,
    ChiEvent,
    DaminggangEvent,
    DapaiEvent,
    JiagangEvent,
    LiqiSuccess,
    LiujuEvent,
    LiujuType,
    MatchEvent,
    NewRoundEvent,
    PengEvent,
    StartMatchEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation import (
    AngangOperation,
    BabeiOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    JiagangOperation,
    LiqiOperation,
    LiujuOperation,
    MatchOperation,
    OperationCandidates,
    PengOperation,
)
from majsoulrpa.screens.match.state import (
    Angang,
    Babei,
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
    "AngangEvent",
    "AngangOperation",
    "Babei",
    "BabeiEvent",
    "BabeiOperation",
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
    "JiagangEvent",
    "JiagangOperation",
    "LiqiOperation",
    "LiqiSuccess",
    "LiujuEvent",
    "LiujuOperation",
    "LiujuType",
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
