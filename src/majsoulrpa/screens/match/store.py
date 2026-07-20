from majsoulrpa.screens.match._metadata import MatchMetadata
from majsoulrpa.screens.match.event import NewRoundEvent, StartMatchEvent
from majsoulrpa.screens.match.state import MatchState, RoundState


class MatchStateStore:
    def __init__(self) -> None:
        self._state: MatchState | None = None

    @property
    def state(self) -> MatchState | None:
        return self._state

    def initialize(
        self,
        metadata: MatchMetadata,
        start_match_event: StartMatchEvent | None,
        new_round_event: NewRoundEvent,
        *,
        has_pending_operation: bool,
    ) -> MatchState:
        if self._state is not None:
            msg = "Match state store is already initialized."
            raise RuntimeError(msg)
        events = (
            (start_match_event, new_round_event)
            if start_match_event is not None
            else (new_round_event,)
        )
        player_count = len(metadata.players)
        round_state = RoundState(
            generation=1,
            step=new_round_event.action_step,
            chang=new_round_event.chang,
            ju=new_round_event.ju,
            ben=new_round_event.ben,
            liqibang=new_round_event.liqibang,
            dora_indicators=new_round_event.dora_indicators,
            left_tile_count=new_round_event.left_tile_count,
            scores=new_round_event.scores,
            shoupai=new_round_event.shoupai,
            zimopai=new_round_event.zimopai,
            he=tuple(() for _ in range(player_count)),
            fulu=tuple(() for _ in range(player_count)),
            num_babei=(0,) * player_count,
            liqi=(False,) * player_count,
            wliqi=(False,) * player_count,
            first_draw=(True,) * player_count,
            yifa=(False,) * player_count,
            lingshang_zimo=(False,) * player_count,
            previous_dapai_seat=None,
            previous_dapai_tile=None,
            has_pending_operation=has_pending_operation,
            events=events,
        )
        self._state = MatchState(
            version=1,
            match_id=metadata.match_id,
            origin=metadata.origin,
            origin_id=metadata.origin_id,
            self_seat=metadata.self_seat,
            players=metadata.players,
            round=round_state,
        )
        return self._state
