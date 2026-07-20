from dataclasses import replace
from typing import assert_never

from majsoulrpa.screens.match._metadata import MatchMetadata
from majsoulrpa.screens.match.event import (
    DapaiEvent,
    MatchEvent,
    NewRoundEvent,
    StartMatchEvent,
)
from majsoulrpa.screens.match.event._common import tile_sort_key
from majsoulrpa.screens.match.state import (
    MatchDapai,
    MatchState,
    RoundState,
)


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

    def apply_event(
        self,
        event: MatchEvent,
        *,
        has_pending_operation: bool,
    ) -> MatchState:
        match event:
            case DapaiEvent():
                return self._apply_dapai(
                    event,
                    has_pending_operation=has_pending_operation,
                )
            case StartMatchEvent() | NewRoundEvent():
                msg = "A match initialization event cannot be applied again."
                raise ValueError(msg)
        assert_never(event)

    def _apply_dapai(
        self,
        event: DapaiEvent,
        *,
        has_pending_operation: bool,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        if event.action_step != round_state.step + 1:
            msg = "ActionDiscardTile step must follow the current round step."
            raise ValueError(msg)
        if event.seat >= len(state.players):
            msg = "ActionDiscardTile seat must identify a player."
            raise ValueError(msg)
        if round_state.previous_dapai_seat is not None:
            msg = "A discard cannot follow an unresolved discard."
            raise ValueError(msg)

        shoupai = list(round_state.shoupai)
        zimopai = round_state.zimopai
        if event.seat == state.self_seat:
            shoupai, zimopai = self._apply_self_dapai(
                event,
                round_state,
                shoupai,
                zimopai,
            )

        he = [list(dapai) for dapai in round_state.he]
        he[event.seat].append(
            MatchDapai(
                tile=event.tile,
                moqie=event.moqie,
                liqi=event.liqi,
                wliqi=event.wliqi,
            ),
        )
        liqi = list(round_state.liqi)
        wliqi = list(round_state.wliqi)
        first_draw = list(round_state.first_draw)
        yifa = list(round_state.yifa)
        lingshang_zimo = list(round_state.lingshang_zimo)
        if event.liqi:
            liqi[event.seat] = True
            yifa[event.seat] = True
        elif event.wliqi:
            wliqi[event.seat] = True
            yifa[event.seat] = True
        else:
            yifa[event.seat] = False
        first_draw[event.seat] = False
        lingshang_zimo[event.seat] = False

        next_round = replace(
            round_state,
            step=event.action_step,
            dora_indicators=(
                event.dora_indicators or round_state.dora_indicators
            ),
            shoupai=tuple(shoupai),
            zimopai=zimopai,
            he=tuple(tuple(dapai) for dapai in he),
            liqi=tuple(liqi),
            wliqi=tuple(wliqi),
            first_draw=tuple(first_draw),
            yifa=tuple(yifa),
            lingshang_zimo=tuple(lingshang_zimo),
            previous_dapai_seat=event.seat,
            previous_dapai_tile=event.tile,
            has_pending_operation=has_pending_operation,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    @staticmethod
    def _apply_self_dapai(
        event: DapaiEvent,
        round_state: RoundState,
        shoupai: list[str],
        zimopai: str | None,
    ) -> tuple[list[str], str | None]:
        if event.moqie:
            if zimopai != event.tile:
                msg = "A self moqie tile must match zimopai."
                raise ValueError(msg)
            return shoupai, None

        try:
            shoupai.remove(event.tile)
        except ValueError:
            # ActionNewRound sorts all 14 dealt tiles and places the
            # rightmost tile in zimopai for presentation. On the
            # dealer's first discard, that tile may therefore be a hand
            # discard even though it is stored separately from shoupai.
            if not (
                event.seat == round_state.ju
                and round_state.first_draw[event.seat]
                and zimopai == event.tile
            ):
                msg = "A self dapai tile must be in the hand."
                raise ValueError(msg) from None
            return shoupai, None

        if zimopai is not None:
            shoupai.append(zimopai)
            shoupai.sort(key=tile_sort_key)
            zimopai = None
        return shoupai, zimopai

    def _require_state(self) -> MatchState:
        if self._state is None:
            msg = "Match state store is not initialized."
            raise RuntimeError(msg)
        return self._state
