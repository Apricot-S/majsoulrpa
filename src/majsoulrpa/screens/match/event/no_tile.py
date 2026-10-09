from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens._json_fields import (
    get_bool,
    get_dict_list,
    get_int,
    get_int_list,
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


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTilePlayer:
    tingpai: bool
    hand: tuple[Tile, ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            tingpai=get_bool(data, "tingpai"),
            hand=tuple(
                validate_tile(tile) for tile in get_str_list(data, "hand")
            ),
        )


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTileScore:
    seat: Seat | None
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
        score = get_int(data, "score")
        return cls(
            seat=(
                validate_seat(get_int(data, "seat")) if score != 0 else None
            ),
            old_scores=tuple(get_int_list(data, "old_scores")),
            delta_scores=tuple(get_int_list(data, "delta_scores")),
            hand=tuple(
                validate_tile(tile) for tile in get_str_list(data, "hand")
            ),
            ming=tuple(get_str_list(data, "ming")),
            dora_indicators=tuple(
                validate_tile(tile) for tile in get_str_list(data, "doras")
            ),
            score=score,
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
                (score.seat is not None and score.seat >= player_count)
                or len(score.old_scores) != player_count
                or len(score.delta_scores) not in (0, player_count)
            ):
                msg = "NoTile score collections must match the player count."
                raise ValueError(msg)
            if score.seat is None:
                continue
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
            liujumanguan=get_bool(data, "liujumanguan"),
            players=tuple(
                NoTilePlayer.from_dict(player)
                for player in get_dict_list(data, "players")
            ),
            scores=tuple(
                NoTileScore.from_dict(score)
                for score in get_dict_list(data, "scores")
            ),
            game_end=get_bool(data, "gameend"),
        )
