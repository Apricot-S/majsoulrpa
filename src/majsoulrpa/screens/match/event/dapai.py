from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event.new_round import _validate_tile

_MAX_SEAT = 3


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiEvent(_MatchEventBase):
    seat: int
    tile: str
    moqie: bool
    liqi: bool
    wliqi: bool
    dora_indicators: tuple[str, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if not 0 <= self.seat <= _MAX_SEAT:
            msg = "Dapai seat must be between 0 and 3."
            raise ValueError(msg)
        _validate_tile(self.tile)
        if self.liqi and self.wliqi:
            msg = "liqi and wliqi must not both be true."
            raise ValueError(msg)
        for tile in self.dora_indicators:
            _validate_tile(tile)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        return cls(
            action_step=action_step,
            seat=_get_int(data, "seat"),
            tile=_get_str(data, "tile"),
            moqie=_get_bool(data, "moqie"),
            liqi=_get_bool(data, "is_liqi"),
            wliqi=_get_bool(data, "is_wliqi"),
            dora_indicators=tuple(_get_str_list(data, "doras")),
        )


def _get_int(data: Mapping[str, JsonValue], name: str) -> int:
    value = data.get(name)
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"ActionDiscardTile.{name} must be an int."
        raise TypeError(msg)
    return value


def _get_str(data: Mapping[str, JsonValue], name: str) -> str:
    value = data.get(name)
    if not isinstance(value, str):
        msg = f"ActionDiscardTile.{name} must be a string."
        raise TypeError(msg)
    return value


def _get_bool(data: Mapping[str, JsonValue], name: str) -> bool:
    value = data.get(name)
    if not isinstance(value, bool):
        msg = f"ActionDiscardTile.{name} must be a bool."
        raise TypeError(msg)
    return value


def _get_str_list(
    data: Mapping[str, JsonValue],
    name: str,
) -> list[str]:
    value = data.get(name)
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        msg = f"ActionDiscardTile.{name} must be a list of strings."
        raise TypeError(msg)
    return value
