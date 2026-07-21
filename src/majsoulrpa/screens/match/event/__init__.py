from majsoulrpa.screens.match.event.chi import ChiEvent
from majsoulrpa.screens.match.event.dapai import DapaiEvent
from majsoulrpa.screens.match.event.liqi_success import LiqiSuccess
from majsoulrpa.screens.match.event.new_round import NewRoundEvent
from majsoulrpa.screens.match.event.start_match import StartMatchEvent
from majsoulrpa.screens.match.event.zimo import ZimoEvent

type MatchEvent = (
    StartMatchEvent | NewRoundEvent | ZimoEvent | DapaiEvent | ChiEvent
)

__all__ = [
    "ChiEvent",
    "DapaiEvent",
    "LiqiSuccess",
    "MatchEvent",
    "NewRoundEvent",
    "StartMatchEvent",
    "ZimoEvent",
]
