from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_int,
    _get_optional_dict,
)
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event.liqi_success import LiqiSuccess
from majsoulrpa.screens.match.types import Seat, validate_seat


class LiujuType(StrEnum):
    JIUZHONGJIUPAI = "jiuzhongjiupai"
    SIFENGLIANDA = "sifenglianda"
    SIGANGSANLE = "sigangsanle"
    SIJIALIQI = "sijialiqi"


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LiujuEvent(_MatchEventBase):
    type: LiujuType
    seat: Seat | None
    liqi_success: LiqiSuccess | None = None

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if self.type is LiujuType.JIUZHONGJIUPAI:
            if self.seat is None:
                msg = "A jiuzhongjiupai event must identify a seat."
                raise ValueError(msg)
        elif self.seat is not None:
            msg = "Only a jiuzhongjiupai event may identify a seat."
            raise ValueError(msg)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        wire_type = _get_int(data, "ActionLiuJu.type")
        match wire_type:
            case 1:
                type_ = LiujuType.JIUZHONGJIUPAI
            case 2:
                type_ = LiujuType.SIFENGLIANDA
            case 3:
                type_ = LiujuType.SIGANGSANLE
            case 4:
                type_ = LiujuType.SIJIALIQI
            case _:
                msg = f"ActionLiuJu.type is not supported: {wire_type}."
                raise ValueError(msg)

        wire_seat = _get_int(data, "ActionLiuJu.seat")
        if type_ is LiujuType.JIUZHONGJIUPAI:
            seat = validate_seat(wire_seat)
        else:
            if wire_seat != 0:
                msg = "ActionLiuJu.seat must be zero for this liuju type."
                raise ValueError(msg)
            seat = None

        liqi = _get_optional_dict(data, "ActionLiuJu.liqi")
        return cls(
            action_step=action_step,
            type=type_,
            seat=seat,
            liqi_success=None if liqi is None else LiqiSuccess.from_dict(liqi),
        )
