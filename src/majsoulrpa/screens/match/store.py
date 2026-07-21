from dataclasses import replace
from typing import assert_never

from majsoulrpa.screens.match._metadata import MatchMetadata
from majsoulrpa.screens.match.event import (
    ChiEvent,
    DapaiEvent,
    LiqiSuccess,
    MatchEvent,
    NewRoundEvent,
    StartMatchEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.event._common import tile_sort_key
from majsoulrpa.screens.match.operation._materialize import (
    materialize_operation_candidates,
)
from majsoulrpa.screens.match.operation._specification import (
    _OperationCandidatesSpecification,
)
from majsoulrpa.screens.match.state import (
    MatchDapai,
    MatchFulu,
    MatchFuluKind,
    MatchState,
    RoundState,
)
from majsoulrpa.screens.match.types import Tile

_FOUR_PLAYER_COUNT = 4


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
        operation_specification: _OperationCandidatesSpecification | None,
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
        operation_candidates = materialize_operation_candidates(
            operation_specification,
            new_round_event,
            new_round_event.shoupai,
            new_round_event.zimopai,
            metadata.self_seat,
        )
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
            operation_candidates=operation_candidates,
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
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        match event:
            case ZimoEvent():
                return self._apply_zimo(event, operation_specification)
            case DapaiEvent():
                return self._apply_dapai(event, operation_specification)
            case ChiEvent():
                return self._apply_chi(event, operation_specification)
            case StartMatchEvent() | NewRoundEvent():
                msg = "A match initialization event cannot be applied again."
                raise ValueError(msg)
        assert_never(event)

    def _apply_zimo(
        self,
        event: ZimoEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        if event.action_step != round_state.step + 1:
            msg = "ActionDealTile step must follow the current round step."
            raise ValueError(msg)
        if event.seat >= len(state.players):
            msg = "ActionDealTile seat must identify a player."
            raise ValueError(msg)
        if round_state.previous_dapai_seat is None:
            msg = "ActionDealTile must follow an unresolved discard."
            raise ValueError(msg)

        zimopai = round_state.zimopai
        if event.seat == state.self_seat:
            if event.tile is None:
                msg = "A self draw must reveal its tile."
                raise ValueError(msg)
            if zimopai is not None:
                msg = "A self draw cannot replace an unresolved drawn tile."
                raise ValueError(msg)
            zimopai = event.tile
        elif event.tile is not None:
            msg = "An opponent draw must conceal its tile."
            raise ValueError(msg)

        scores, liqibang = self._apply_liqi_success(
            event.liqi_success,
            round_state.scores,
            round_state.liqibang,
            len(state.players),
        )

        operation_candidates = materialize_operation_candidates(
            operation_specification,
            event,
            round_state.shoupai,
            zimopai,
            state.self_seat,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            dora_indicators=(
                event.dora_indicators or round_state.dora_indicators
            ),
            left_tile_count=event.left_tile_count,
            scores=scores,
            liqibang=liqibang,
            zimopai=zimopai,
            previous_dapai_seat=None,
            previous_dapai_tile=None,
            operation_candidates=operation_candidates,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_dapai(
        self,
        event: DapaiEvent,
        operation_specification: _OperationCandidatesSpecification | None,
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

        next_shoupai = tuple(shoupai)
        operation_candidates = materialize_operation_candidates(
            operation_specification,
            event,
            next_shoupai,
            zimopai,
            state.self_seat,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            dora_indicators=(
                event.dora_indicators or round_state.dora_indicators
            ),
            shoupai=next_shoupai,
            zimopai=zimopai,
            he=tuple(tuple(dapai) for dapai in he),
            liqi=tuple(liqi),
            wliqi=tuple(wliqi),
            first_draw=tuple(first_draw),
            yifa=tuple(yifa),
            lingshang_zimo=tuple(lingshang_zimo),
            previous_dapai_seat=event.seat,
            previous_dapai_tile=event.tile,
            operation_candidates=operation_candidates,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_chi(
        self,
        event: ChiEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if player_count != _FOUR_PLAYER_COUNT:
            msg = "A chi is only valid in a four-player match."
            raise ValueError(msg)
        if event.action_step != round_state.step + 1:
            msg = "ActionChiPengGang step must follow the current round step."
            raise ValueError(msg)
        if event.seat >= player_count or event.from_seat >= player_count:
            msg = "ActionChiPengGang seats must identify players."
            raise ValueError(msg)
        if event.from_seat != round_state.previous_dapai_seat:
            msg = "A chi must claim the unresolved discard."
            raise ValueError(msg)
        if event.tile != round_state.previous_dapai_tile:
            msg = "A chi claimed tile must match the unresolved discard."
            raise ValueError(msg)
        if event.from_seat != (event.seat - 1) % player_count:
            msg = "A chi must claim a discard from the preceding player."
            raise ValueError(msg)
        if round_state.zimopai is not None:
            msg = "A chi cannot occur while a self draw is unresolved."
            raise ValueError(msg)
        if (
            event.seat != state.self_seat
            and operation_specification is not None
        ):
            msg = "An opponent chi cannot provide self operations."
            raise ValueError(msg)

        shoupai = list(round_state.shoupai)
        if event.seat == state.self_seat:
            for tile in event.consumed:
                try:
                    shoupai.remove(tile)
                except ValueError:
                    msg = "A self chi must consume tiles in the hand."
                    raise ValueError(msg) from None

        fulu = [list(player_fulu) for player_fulu in round_state.fulu]
        fulu[event.seat].append(
            MatchFulu(
                kind=MatchFuluKind.CHI,
                tiles=(*event.consumed, event.tile),
                from_seat=event.from_seat,
            )
        )
        scores, liqibang = self._apply_liqi_success(
            event.liqi_success,
            round_state.scores,
            round_state.liqibang,
            player_count,
        )

        next_shoupai = tuple(shoupai)
        operation_candidates = materialize_operation_candidates(
            operation_specification,
            event,
            next_shoupai,
            None,
            state.self_seat,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            scores=scores,
            liqibang=liqibang,
            shoupai=next_shoupai,
            fulu=tuple(tuple(player_fulu) for player_fulu in fulu),
            first_draw=(False,) * player_count,
            yifa=(False,) * player_count,
            previous_dapai_seat=None,
            previous_dapai_tile=None,
            operation_candidates=operation_candidates,
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
        shoupai: list[Tile],
        zimopai: Tile | None,
    ) -> tuple[list[Tile], Tile | None]:
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

    @staticmethod
    def _apply_liqi_success(
        liqi_success: LiqiSuccess | None,
        scores: tuple[int, ...],
        liqibang: int,
        player_count: int,
    ) -> tuple[tuple[int, ...], int]:
        if liqi_success is None:
            return scores, liqibang
        if liqi_success.seat >= player_count:
            msg = "LiQiSuccess seat must identify a player."
            raise ValueError(msg)
        mutable_scores = list(scores)
        mutable_scores[liqi_success.seat] = liqi_success.score
        return tuple(mutable_scores), liqi_success.liqibang

    def _require_state(self) -> MatchState:
        if self._state is None:
            msg = "Match state store is not initialized."
            raise RuntimeError(msg)
        return self._state
