from majsoulrpa.screens.match.event.angang import AngangEvent
from majsoulrpa.screens.match.event.babei import BabeiEvent
from majsoulrpa.screens.match.event.chi import ChiEvent
from majsoulrpa.screens.match.event.daminggang import DaminggangEvent
from majsoulrpa.screens.match.event.dapai import DapaiEvent
from majsoulrpa.screens.match.event.hule import Hule, HuleEvent, HuleFan
from majsoulrpa.screens.match.event.jiagang import JiagangEvent
from majsoulrpa.screens.match.event.liqi_success import LiqiSuccess
from majsoulrpa.screens.match.event.liuju import LiujuEvent, LiujuType
from majsoulrpa.screens.match.event.new_round import NewRoundEvent
from majsoulrpa.screens.match.event.peng import PengEvent
from majsoulrpa.screens.match.event.start_match import StartMatchEvent
from majsoulrpa.screens.match.event.zimo import ZimoEvent

type MatchEvent = (
    StartMatchEvent
    | NewRoundEvent
    | ZimoEvent
    | DapaiEvent
    | ChiEvent
    | PengEvent
    | DaminggangEvent
    | AngangEvent
    | JiagangEvent
    | BabeiEvent
    | LiujuEvent
    | HuleEvent
)

__all__ = [
    "AngangEvent",
    "BabeiEvent",
    "ChiEvent",
    "DaminggangEvent",
    "DapaiEvent",
    "Hule",
    "HuleEvent",
    "HuleFan",
    "JiagangEvent",
    "LiqiSuccess",
    "LiujuEvent",
    "LiujuType",
    "MatchEvent",
    "NewRoundEvent",
    "PengEvent",
    "StartMatchEvent",
    "ZimoEvent",
]
