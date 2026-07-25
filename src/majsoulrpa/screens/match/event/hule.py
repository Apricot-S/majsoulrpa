from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_bool,
    _get_dict_list,
    _get_int,
    _get_int_list,
    _get_optional_dict,
    _get_str,
    _get_str_list,
)
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import MAX_DORA_INDICATORS
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HuleFan:
    name: str
    value: int
    id: int

    def __post_init__(self) -> None:
        if self.value < 0:
            msg = "Hule fan value must be nonnegative."
            raise ValueError(msg)
        if self.id < 0:
            msg = "Hule fan ID must be nonnegative."
            raise ValueError(msg)

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            name=_get_str(data, "FanInfo.name"),
            value=_get_int(data, "FanInfo.val"),
            id=_get_int(data, "FanInfo.id"),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class Hule:
    hand: tuple[Tile, ...]
    ming: tuple[str, ...]
    tile: Tile
    seat: Seat
    zimo: bool
    qinjia: bool
    liqi: bool
    doras: tuple[Tile, ...]
    li_doras: tuple[Tile, ...]
    yiman: bool
    count: int
    fans: tuple[HuleFan, ...]
    fu: int
    title: str
    point_rong: int
    point_zimo_qin: int
    point_zimo_xian: int
    title_id: int
    point_sum: int
    dadian: int
    baopai: int
    baopai_seats: tuple[Seat, ...]

    def __post_init__(self) -> None:
        values = (
            self.count,
            self.fu,
            self.point_rong,
            self.point_zimo_qin,
            self.point_zimo_xian,
            self.title_id,
            self.point_sum,
            self.dadian,
            self.baopai,
        )
        if any(value < 0 for value in values):
            msg = "Hule numeric values must be nonnegative."
            raise ValueError(msg)

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            hand=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "HuleInfo.hand")
            ),
            ming=tuple(_get_str_list(data, "HuleInfo.ming")),
            tile=validate_tile(_get_str(data, "HuleInfo.hu_tile")),
            seat=validate_seat(_get_int(data, "HuleInfo.seat")),
            zimo=_get_bool(data, "HuleInfo.zimo"),
            qinjia=_get_bool(data, "HuleInfo.qinjia"),
            liqi=_get_bool(data, "HuleInfo.liqi"),
            doras=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "HuleInfo.doras")
            ),
            li_doras=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "HuleInfo.li_doras")
            ),
            yiman=_get_bool(data, "HuleInfo.yiman"),
            count=_get_int(data, "HuleInfo.count"),
            fans=tuple(
                HuleFan.from_dict(fan)
                for fan in _get_dict_list(data, "HuleInfo.fans")
            ),
            fu=_get_int(data, "HuleInfo.fu"),
            title=_get_str(data, "HuleInfo.title"),
            point_rong=_get_int(data, "HuleInfo.point_rong"),
            point_zimo_qin=_get_int(data, "HuleInfo.point_zimo_qin"),
            point_zimo_xian=_get_int(data, "HuleInfo.point_zimo_xian"),
            title_id=_get_int(data, "HuleInfo.title_id"),
            point_sum=_get_int(data, "HuleInfo.point_sum"),
            dadian=_get_int(data, "HuleInfo.dadian"),
            baopai=_get_int(data, "HuleInfo.baopai"),
            baopai_seats=tuple(
                validate_seat(seat)
                for seat in _get_int_list(data, "HuleInfo.baopai_seats")
            ),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HuleEvent(_MatchEventBase):
    hules: tuple[Hule, ...]
    old_scores: tuple[int, ...]
    delta_scores: tuple[int, ...]
    scores: tuple[int, ...]
    dora_indicators: tuple[Tile, ...]
    game_end_scores: tuple[int, ...] | None
    baopai: int

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if not self.hules:
            msg = "hules must not be empty."
            raise ValueError(msg)
        score_count = len(self.scores)
        if (
            score_count not in (3, 4)
            or len(self.old_scores) != score_count
            or len(self.delta_scores) != score_count
        ):
            msg = "Hule score collections must contain three or four values."
            raise ValueError(msg)
        if (
            self.game_end_scores is not None
            and len(self.game_end_scores) != score_count
        ):
            msg = "Game-end scores must match the Hule score count."
            raise ValueError(msg)
        if not 1 <= len(self.dora_indicators) <= MAX_DORA_INDICATORS:
            msg = "dora_indicators must contain between one and five tiles."
            raise ValueError(msg)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        game_end = _get_optional_dict(data, "ActionHule.gameend")
        return cls(
            action_step=action_step,
            hules=tuple(
                Hule.from_dict(hule)
                for hule in _get_dict_list(data, "ActionHule.hules")
            ),
            old_scores=tuple(_get_int_list(data, "ActionHule.old_scores")),
            delta_scores=tuple(_get_int_list(data, "ActionHule.delta_scores")),
            scores=tuple(_get_int_list(data, "ActionHule.scores")),
            dora_indicators=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "ActionHule.doras")
            ),
            game_end_scores=(
                None
                if game_end is None
                else tuple(_get_int_list(game_end, "GameEnd.scores"))
            ),
            baopai=_get_int(data, "ActionHule.baopai"),
        )
