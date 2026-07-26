from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_bool,
    _get_dict_list,
    _get_int,
    _get_int_list,
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
class NoTilePlayer:
    tingpai: bool
    hand: tuple[Tile, ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            tingpai=_get_bool(data, "NoTilePlayerInfo.tingpai"),
            hand=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "NoTilePlayerInfo.hand")
            ),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTileScore:
    seat: Seat
    old_scores: tuple[int, ...]
    delta_scores: tuple[int, ...]
    hand: tuple[Tile, ...]
    ming: tuple[str, ...]
    dora_indicators: tuple[Tile, ...]
    score: int

    def __post_init__(self) -> None:
        if self.score < 0:
            msg = "NoTile score must be nonnegative."
            raise ValueError(msg)
        if len(self.dora_indicators) > MAX_DORA_INDICATORS:
            msg = "dora_indicators must contain at most five tiles."
            raise ValueError(msg)

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            seat=validate_seat(_get_int(data, "NoTileScoreInfo.seat")),
            old_scores=tuple(
                _get_int_list(data, "NoTileScoreInfo.old_scores")
            ),
            delta_scores=tuple(
                _get_int_list(data, "NoTileScoreInfo.delta_scores")
            ),
            hand=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "NoTileScoreInfo.hand")
            ),
            ming=tuple(_get_str_list(data, "NoTileScoreInfo.ming")),
            dora_indicators=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "NoTileScoreInfo.doras")
            ),
            score=_get_int(data, "NoTileScoreInfo.score"),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTileEvent(_MatchEventBase):
    liujumanguan: bool
    players: tuple[NoTilePlayer, ...]
    scores: tuple[NoTileScore, ...]
    game_end: bool

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        player_count = len(self.players)
        if player_count not in (3, 4):
            msg = "players must contain three or four players."
            raise ValueError(msg)

        score_seats: set[Seat] = set()
        for score in self.scores:
            if (
                score.seat >= player_count
                or len(score.old_scores) != player_count
                or len(score.delta_scores) != player_count
            ):
                msg = "NoTile score collections must match the player count."
                raise ValueError(msg)
            if score.seat in score_seats:
                msg = "NoTile score seats must be unique."
                raise ValueError(msg)
            score_seats.add(score.seat)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        return cls(
            action_step=action_step,
            liujumanguan=_get_bool(data, "ActionNoTile.liujumanguan"),
            players=tuple(
                NoTilePlayer.from_dict(player)
                for player in _get_dict_list(data, "ActionNoTile.players")
            ),
            scores=tuple(
                NoTileScore.from_dict(score)
                for score in _get_dict_list(data, "ActionNoTile.scores")
            ),
            game_end=_get_bool(data, "ActionNoTile.gameend"),
        )
