from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens._json_fields import (
    get_bool,
    get_dict_list,
    get_int,
    get_int_list,
    get_str,
    get_str_list,
)
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import MAX_DORA_INDICATORS
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)

_BAOPAI_SEAT_VALUES = range(1, 5)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HuleFan:
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
            value=get_int(data, "val"),
            id=get_int(data, "id"),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class Hule:
    hand: tuple[Tile, ...]
    ming: tuple[str, ...]
    hu_tile: Tile
    seat: Seat
    zimo: bool
    qinjia: bool
    liqi: bool
    dora_indicators: tuple[Tile, ...]
    li_dora_indicators: tuple[Tile, ...]
    yiman: bool
    count: int
    fans: tuple[HuleFan, ...]
    fu: int
    point_rong: int
    point_zimo_qin: int
    point_zimo_xian: int
    title_id: int
    point_sum: int
    dadian: int
    baopai_seat: Seat | None
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
        )
        if any(value < 0 for value in values):
            msg = "Hule numeric values must be nonnegative."
            raise ValueError(msg)
        if len(self.dora_indicators) > MAX_DORA_INDICATORS:
            msg = "dora_indicators must contain at most five tiles."
            raise ValueError(msg)
        if len(self.li_dora_indicators) > MAX_DORA_INDICATORS:
            msg = "li_dora_indicators must contain at most five tiles."
            raise ValueError(msg)

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            hand=tuple(
                validate_tile(tile) for tile in get_str_list(data, "hand")
            ),
            ming=tuple(get_str_list(data, "ming")),
            hu_tile=validate_tile(get_str(data, "hu_tile")),
            seat=validate_seat(get_int(data, "seat")),
            zimo=get_bool(data, "zimo"),
            qinjia=get_bool(data, "qinjia"),
            liqi=get_bool(data, "liqi"),
            dora_indicators=tuple(
                validate_tile(tile) for tile in get_str_list(data, "doras")
            ),
            li_dora_indicators=tuple(
                validate_tile(tile) for tile in get_str_list(data, "li_doras")
            ),
            yiman=get_bool(data, "yiman"),
            count=get_int(data, "count"),
            fans=tuple(
                HuleFan.from_dict(fan) for fan in get_dict_list(data, "fans")
            ),
            fu=get_int(data, "fu"),
            point_rong=get_int(data, "point_rong"),
            point_zimo_qin=get_int(data, "point_zimo_qin"),
            point_zimo_xian=get_int(data, "point_zimo_xian"),
            title_id=get_int(data, "title_id"),
            point_sum=get_int(data, "point_sum"),
            dadian=get_int(data, "dadian"),
            baopai_seat=_decode_baopai_seat(get_int(data, "baopai")),
            baopai_seats=tuple(
                validate_seat(seat)
                for seat in get_int_list(data, "baopai_seats")
            ),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HuleEvent(_MatchEventBase):
    hules: tuple[Hule, ...]
    old_scores: tuple[int, ...]
    delta_scores: tuple[int, ...]
    scores: tuple[int, ...]
    baopai_seat: Seat | None

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

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        return cls(
            action_step=action_step,
            hules=tuple(
                Hule.from_dict(hule) for hule in get_dict_list(data, "hules")
            ),
            old_scores=tuple(get_int_list(data, "old_scores")),
            delta_scores=tuple(get_int_list(data, "delta_scores")),
            scores=tuple(get_int_list(data, "scores")),
            baopai_seat=_decode_baopai_seat(get_int(data, "baopai")),
        )


def _decode_baopai_seat(value: int) -> Seat | None:
    if value == 0:
        return None
    if value in _BAOPAI_SEAT_VALUES:
        return validate_seat(value - 1)
    msg = "baopai must be between 0 and 4."
    raise ValueError(msg)
