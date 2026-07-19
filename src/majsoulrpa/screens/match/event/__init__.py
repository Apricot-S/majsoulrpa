from majsoulrpa.screens.match.event.new_round import NewRoundEvent
from majsoulrpa.screens.match.event.start_match import StartMatchEvent

type MatchEvent = StartMatchEvent | NewRoundEvent

__all__ = ["MatchEvent", "NewRoundEvent", "StartMatchEvent"]
