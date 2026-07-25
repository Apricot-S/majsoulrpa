from dataclasses import replace
from typing import assert_never

from majsoulrpa.screens.match._common import (
    is_preceding_seat,
    tile_sort_key,
)
from majsoulrpa.screens.match._metadata import MatchMetadata
from majsoulrpa.screens.match.event import (
    AngangEvent,
    BabeiEvent,
    ChiEvent,
    DaminggangEvent,
    DapaiEvent,
    HuleEvent,
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
from majsoulrpa.screens.match.operation._materialize import (
    materialize_operation_candidates,
)
from majsoulrpa.screens.match.operation._specification import (
    _OperationCandidatesSpecification,
)
from majsoulrpa.screens.match.state import (
    Angang,
    Babei,
    Chi,
    Daminggang,
    Dapai,
    Fulu,
    Jiagang,
    MatchState,
    Peng,
    RoundState,
)
from majsoulrpa.screens.match.types import Tile


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
            (),
            metadata.self_seat,
            player_count,
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
            babei=tuple(() for _ in range(player_count)),
            liqi=(False,) * player_count,
            wliqi=(False,) * player_count,
            first_draw=(True,) * player_count,
            yifa=(False,) * player_count,
            lingshang_zimo=(False,) * player_count,
            previous_dapai=None,
            previous_qianggang=None,
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
            case PengEvent():
                return self._apply_peng(event, operation_specification)
            case DaminggangEvent():
                return self._apply_daminggang(event, operation_specification)
            case AngangEvent():
                return self._apply_angang(event, operation_specification)
            case JiagangEvent():
                return self._apply_jiagang(event, operation_specification)
            case BabeiEvent():
                return self._apply_babei(event, operation_specification)
            case LiujuEvent():
                return self._apply_liuju(event)
            case HuleEvent():
                return self._apply_hule(event)
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
        previous_event = round_state.events[-1]
        follows_lingshang_operation = (
            isinstance(
                previous_event,
                DaminggangEvent | AngangEvent | JiagangEvent | BabeiEvent,
            )
            and previous_event.seat == event.seat
            and round_state.lingshang_zimo[event.seat]
        )
        if (
            round_state.previous_dapai is None
            and not follows_lingshang_operation
        ):
            msg = (
                "ActionDealTile must follow an unresolved discard "
                "or lingshang operation."
            )
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
            round_state.fulu[state.self_seat],
            state.self_seat,
            len(state.players),
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
            previous_dapai=None,
            previous_qianggang=None,
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
        if round_state.previous_dapai is not None:
            msg = "A discard cannot follow an unresolved discard."
            raise ValueError(msg)
        if round_state.previous_qianggang is not None:
            msg = "A discard cannot follow an unresolved qianggang target."
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
            Dapai(
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
            round_state.fulu[state.self_seat],
            state.self_seat,
            len(state.players),
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
            previous_dapai=(event.seat, event.tile),
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
        player_count = len(state.players)
        if player_count != 4:  # noqa: PLR2004
            msg = "A chi is only valid in a four-player match."
            raise ValueError(msg)
        if not is_preceding_seat(
            event.from_seat,
            relative_to=event.seat,
            player_count=player_count,
        ):
            msg = "A chi must claim a discard from the preceding player."
            raise ValueError(msg)

        return self._apply_fulu(
            event,
            Chi(
                from_seat=event.from_seat,
                tile=event.tile,
                consumed=event.consumed,
            ),
            operation_specification,
        )

    def _apply_peng(
        self,
        event: PengEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        return self._apply_fulu(
            event,
            Peng(
                from_seat=event.from_seat,
                tile=event.tile,
                consumed=event.consumed,
            ),
            operation_specification,
        )

    def _apply_daminggang(
        self,
        event: DaminggangEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        return self._apply_fulu(
            event,
            Daminggang(
                from_seat=event.from_seat,
                tile=event.tile,
                consumed=event.consumed,
            ),
            operation_specification,
        )

    def _apply_angang(
        self,
        event: AngangEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if event.action_step != round_state.step + 1:
            msg = (
                "ActionAnGangAddGang step must follow the current round step."
            )
            raise ValueError(msg)
        if event.seat >= player_count:
            msg = "ActionAnGangAddGang seat must identify a player."
            raise ValueError(msg)
        if round_state.previous_dapai is not None:
            msg = "An angang cannot follow an unresolved discard."
            raise ValueError(msg)
        if round_state.previous_qianggang is not None:
            msg = "An angang cannot follow an unresolved qianggang target."
            raise ValueError(msg)
        shoupai = list(round_state.shoupai)
        zimopai = round_state.zimopai
        if event.seat == state.self_seat:
            if zimopai is None:
                msg = "A self angang must follow a self draw."
                raise ValueError(msg)
            expected_kind = event.consumed[3]
            expected_tiles = {expected_kind}
            if expected_kind in {"5m", "5p", "5s"}:
                expected_tiles.add(Tile(f"0{expected_kind[1]}"))
            matching_tiles = sum(tile in expected_tiles for tile in shoupai)
            zimopai_matches = zimopai is not None and zimopai in expected_tiles
            if matching_tiles + int(zimopai_matches) != 4:  # noqa: PLR2004
                msg = "A self angang must consume four tiles of one kind."
                raise ValueError(msg)
            shoupai = [tile for tile in shoupai if tile not in expected_tiles]
            if zimopai_matches:
                zimopai = None
            else:
                shoupai.append(zimopai)
                shoupai.sort(key=tile_sort_key)
                zimopai = None
        elif zimopai is not None:
            msg = "An opponent angang cannot occur during a self draw."
            raise ValueError(msg)

        fulu = [list(player_fulu) for player_fulu in round_state.fulu]
        fulu[event.seat].append(Angang(consumed=event.consumed))
        next_fulu = tuple(tuple(player_fulu) for player_fulu in fulu)
        lingshang_zimo = list(round_state.lingshang_zimo)
        lingshang_zimo[event.seat] = True
        next_shoupai = tuple(shoupai)
        operation_candidates = materialize_operation_candidates(
            operation_specification,
            event,
            next_shoupai,
            zimopai,
            next_fulu[state.self_seat],
            state.self_seat,
            player_count,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            dora_indicators=(
                event.dora_indicators or round_state.dora_indicators
            ),
            shoupai=next_shoupai,
            zimopai=zimopai,
            fulu=next_fulu,
            first_draw=(False,) * player_count,
            yifa=(False,) * player_count,
            lingshang_zimo=tuple(lingshang_zimo),
            previous_qianggang=(event.seat, event.consumed[0]),
            operation_candidates=operation_candidates,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_jiagang(
        self,
        event: JiagangEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if event.action_step != round_state.step + 1:
            msg = (
                "ActionAnGangAddGang step must follow the current round step."
            )
            raise ValueError(msg)
        if event.seat >= player_count:
            msg = "ActionAnGangAddGang seat must identify a player."
            raise ValueError(msg)
        if round_state.previous_dapai is not None:
            msg = "A jiagang cannot follow an unresolved discard."
            raise ValueError(msg)
        if round_state.previous_qianggang is not None:
            msg = "A jiagang cannot follow an unresolved qianggang target."
            raise ValueError(msg)

        player_fulu = round_state.fulu[event.seat]
        added_tiles = {event.added}
        if event.added in {"0m", "5m", "0p", "5p", "0s", "5s"}:
            added_tiles = {
                Tile(f"0{event.added[1]}"),
                Tile(f"5{event.added[1]}"),
            }
        matching_pengs = [
            (index, entry)
            for index, entry in enumerate(player_fulu)
            if isinstance(entry, Peng) and entry.tile in added_tiles
        ]
        if len(matching_pengs) != 1:
            msg = "A jiagang must replace exactly one matching peng."
            raise ValueError(msg)
        peng_index, peng = matching_pengs[0]

        shoupai = list(round_state.shoupai)
        zimopai = round_state.zimopai
        if event.seat == state.self_seat:
            if zimopai is None:
                msg = "A self jiagang must follow a self draw."
                raise ValueError(msg)
            if zimopai == event.added:
                zimopai = None
            else:
                try:
                    shoupai.remove(event.added)
                except ValueError:
                    msg = (
                        "A self jiagang must add a tile from the hand "
                        "or drawn tile."
                    )
                    raise ValueError(msg) from None
                shoupai.append(zimopai)
                shoupai.sort(key=tile_sort_key)
                zimopai = None
        elif zimopai is not None:
            msg = "An opponent jiagang cannot occur during a self draw."
            raise ValueError(msg)

        next_player_fulu = list(player_fulu)
        next_player_fulu[peng_index] = Jiagang(
            from_seat=peng.from_seat,
            tile=peng.tile,
            consumed=peng.consumed,
            added=event.added,
        )
        fulu = list(round_state.fulu)
        fulu[event.seat] = tuple(next_player_fulu)
        next_fulu = tuple(fulu)

        lingshang_zimo = list(round_state.lingshang_zimo)
        lingshang_zimo[event.seat] = True
        next_shoupai = tuple(shoupai)
        operation_candidates = materialize_operation_candidates(
            operation_specification,
            event,
            next_shoupai,
            zimopai,
            next_fulu[state.self_seat],
            state.self_seat,
            player_count,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            dora_indicators=(
                event.dora_indicators or round_state.dora_indicators
            ),
            shoupai=next_shoupai,
            zimopai=zimopai,
            fulu=next_fulu,
            first_draw=(False,) * player_count,
            yifa=(False,) * player_count,
            lingshang_zimo=tuple(lingshang_zimo),
            previous_qianggang=(event.seat, event.added),
            operation_candidates=operation_candidates,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_babei(
        self,
        event: BabeiEvent,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if player_count != 3:  # noqa: PLR2004
            msg = "ActionBaBei is only valid in a three-player match."
            raise ValueError(msg)
        if event.action_step != round_state.step + 1:
            msg = "ActionBaBei step must follow the current round step."
            raise ValueError(msg)
        if event.seat >= player_count:
            msg = "ActionBaBei seat must identify a player."
            raise ValueError(msg)
        if round_state.previous_dapai is not None:
            msg = "A babei cannot follow an unresolved discard."
            raise ValueError(msg)
        if round_state.previous_qianggang is not None:
            msg = "A babei cannot follow an unresolved qianggang target."
            raise ValueError(msg)

        north = Tile("4z")
        shoupai = list(round_state.shoupai)
        zimopai = round_state.zimopai
        if event.seat == state.self_seat:
            if zimopai is None:
                msg = "A self babei must follow a self draw."
                raise ValueError(msg)
            if event.moqie:
                if zimopai != north:
                    msg = "A self moqie babei must consume the drawn north."
                    raise ValueError(msg)
            else:
                try:
                    shoupai.remove(north)
                except ValueError:
                    msg = "A self hand babei must consume a north in the hand."
                    raise ValueError(msg) from None
                shoupai.append(zimopai)
                shoupai.sort(key=tile_sort_key)
            zimopai = None
        elif zimopai is not None:
            msg = "An opponent babei cannot occur during a self draw."
            raise ValueError(msg)

        babei = [list(player_babei) for player_babei in round_state.babei]
        babei[event.seat].append(Babei(moqie=event.moqie))
        next_babei = tuple(tuple(player_babei) for player_babei in babei)
        lingshang_zimo = list(round_state.lingshang_zimo)
        lingshang_zimo[event.seat] = True
        next_shoupai = tuple(shoupai)
        operation_candidates = materialize_operation_candidates(
            operation_specification,
            event,
            next_shoupai,
            zimopai,
            round_state.fulu[state.self_seat],
            state.self_seat,
            player_count,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            dora_indicators=(
                event.dora_indicators or round_state.dora_indicators
            ),
            shoupai=next_shoupai,
            zimopai=zimopai,
            babei=next_babei,
            first_draw=(False,) * player_count,
            yifa=(False,) * player_count,
            lingshang_zimo=tuple(lingshang_zimo),
            previous_qianggang=(event.seat, north),
            operation_candidates=operation_candidates,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_liuju(self, event: LiujuEvent) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if event.action_step != round_state.step + 1:
            msg = "ActionLiuJu step must follow the current round step."
            raise ValueError(msg)
        if event.type is LiujuType.JIUZHONGJIUPAI:
            if event.seat is None or event.seat >= player_count:
                msg = "A jiuzhongjiupai seat must identify a player."
                raise ValueError(msg)
            if not round_state.first_draw[event.seat]:
                msg = "A jiuzhongjiupai must occur during the first draw."
                raise ValueError(msg)

        scores, liqibang = self._apply_liqi_success(
            event.liqi_success,
            round_state.scores,
            round_state.liqibang,
            player_count,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            scores=scores,
            liqibang=liqibang,
            previous_dapai=None,
            previous_qianggang=None,
            operation_candidates=None,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_hule(self, event: HuleEvent) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if event.action_step != round_state.step + 1:
            msg = "ActionHule step must follow the current round step."
            raise ValueError(msg)
        if len(event.scores) != player_count:
            msg = "ActionHule scores must identify every player."
            raise ValueError(msg)
        if event.old_scores != round_state.scores:
            msg = "ActionHule old scores must match the current scores."
            raise ValueError(msg)
        if (
            tuple(
                old_score + delta_score
                for old_score, delta_score in zip(
                    event.old_scores,
                    event.delta_scores,
                    strict=True,
                )
            )
            != event.scores
        ):
            msg = "ActionHule score deltas must produce its scores."
            raise ValueError(msg)

        hule_seats = tuple(hule.seat for hule in event.hules)
        if len(hule_seats) != len(set(hule_seats)):
            msg = "ActionHule winners must be unique."
            raise ValueError(msg)
        for hule in event.hules:
            if hule.seat >= player_count:
                msg = "A hule seat must identify a player."
                raise ValueError(msg)
            if hule.qinjia is not (hule.seat == round_state.ju):
                msg = "Hule qinjia must match the round dealer."
                raise ValueError(msg)

        if len(event.hules) == 1 and event.hules[0].zimo:
            hule = event.hules[0]
            previous_event = round_state.events[-1]
            match previous_event:
                case ZimoEvent():
                    if previous_event.seat != hule.seat:
                        msg = "A zimohu must follow the winner's draw."
                        raise ValueError(msg)
                    if (
                        previous_event.tile is not None
                        and previous_event.tile != hule.hu_tile
                    ):
                        msg = "A zimohu tile must match the preceding draw."
                        raise ValueError(msg)
                case NewRoundEvent():
                    if hule.seat != round_state.ju:
                        msg = "A hule following the deal must be tenhou."
                        raise ValueError(msg)
                    if (
                        round_state.zimopai is not None
                        and round_state.zimopai != hule.hu_tile
                    ):
                        msg = (
                            "A tenhou tile must match the dealt winning tile."
                        )
                        raise ValueError(msg)
                case _:
                    msg = "A zimohu must follow a draw or the initial deal."
                    raise ValueError(msg)
        elif all(not hule.zimo for hule in event.hules):
            unresolved_targets = tuple(
                target
                for target in (
                    round_state.previous_dapai,
                    round_state.previous_qianggang,
                )
                if target is not None
            )
            if len(unresolved_targets) != 1:
                msg = "A rong must follow exactly one unresolved target."
                raise ValueError(msg)
            from_seat, hu_tile = unresolved_targets[0]
            for hule in event.hules:
                if hule.seat == from_seat:
                    msg = "A rong winner must differ from the source seat."
                    raise ValueError(msg)
                if hule.hu_tile != hu_tile:
                    msg = "A rong tile must match the unresolved target."
                    raise ValueError(msg)
        else:
            msg = "Zimohu and rong must not coexist in one ActionHule."
            raise ValueError(msg)

        next_round = replace(
            round_state,
            step=event.action_step,
            scores=event.scores,
            previous_dapai=None,
            previous_qianggang=None,
            operation_candidates=None,
            events=(*round_state.events, event),
        )
        self._state = replace(
            state,
            version=state.version + 1,
            round=next_round,
        )
        return self._state

    def _apply_fulu(
        self,
        event: ChiEvent | PengEvent | DaminggangEvent,
        fulu_entry: Fulu,
        operation_specification: _OperationCandidatesSpecification | None,
    ) -> MatchState:
        state = self._require_state()
        round_state = state.round
        player_count = len(state.players)
        if event.action_step != round_state.step + 1:
            msg = "ActionChiPengGang step must follow the current round step."
            raise ValueError(msg)
        if event.seat >= player_count or event.from_seat >= player_count:
            msg = "ActionChiPengGang seats must identify players."
            raise ValueError(msg)
        previous_dapai = round_state.previous_dapai
        if previous_dapai is None or event.from_seat != previous_dapai[0]:
            msg = "A call must claim the unresolved discard."
            raise ValueError(msg)
        if event.tile != previous_dapai[1]:
            msg = "A called tile must match the unresolved discard."
            raise ValueError(msg)
        if round_state.zimopai is not None:
            msg = "A call cannot occur while a self draw is unresolved."
            raise ValueError(msg)
        if round_state.previous_qianggang is not None:
            msg = "A call cannot follow an unresolved qianggang target."
            raise ValueError(msg)
        if (
            event.seat != state.self_seat
            and operation_specification is not None
        ):
            msg = "An opponent call cannot provide self operations."
            raise ValueError(msg)

        shoupai = list(round_state.shoupai)
        if event.seat == state.self_seat:
            for tile in event.consumed:
                try:
                    shoupai.remove(tile)
                except ValueError:
                    msg = "A self call must consume tiles in the hand."
                    raise ValueError(msg) from None

        fulu = [list(player_fulu) for player_fulu in round_state.fulu]
        fulu[event.seat].append(fulu_entry)
        next_fulu = tuple(tuple(player_fulu) for player_fulu in fulu)
        lingshang_zimo = list(round_state.lingshang_zimo)
        if isinstance(event, DaminggangEvent):
            lingshang_zimo[event.seat] = True
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
            next_fulu[state.self_seat],
            state.self_seat,
            player_count,
        )
        next_round = replace(
            round_state,
            step=event.action_step,
            scores=scores,
            liqibang=liqibang,
            shoupai=next_shoupai,
            fulu=next_fulu,
            first_draw=(False,) * player_count,
            yifa=(False,) * player_count,
            lingshang_zimo=tuple(lingshang_zimo),
            previous_dapai=None,
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
