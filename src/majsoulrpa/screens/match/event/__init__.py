from majsoulrpa.screens.match.event.dapai import DapaiEvent
from majsoulrpa.screens.match.event.new_round import NewRoundEvent
from majsoulrpa.screens.match.event.start_match import StartMatchEvent

type MatchEvent = StartMatchEvent | NewRoundEvent | DapaiEvent

__all__ = ["DapaiEvent", "MatchEvent", "NewRoundEvent", "StartMatchEvent"]
