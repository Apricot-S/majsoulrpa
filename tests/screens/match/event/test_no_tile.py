import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match import (
    NoTileEvent,
    NoTilePlayer,
    NoTileScore,
    validate_seat,
    validate_tile,
)


def test_no_tile_event_from_dict() -> None:
    event = NoTileEvent.from_dict(
        8,
        {
            "liujumanguan": True,
            "players": [
                {
                    "tingpai": True,
                    "hand": ["1m", "2m", "3m"],
                    "tings": [
                        {
                            "tile": "0p",
                            "haveyi": True,
                            "yiman": False,
                            "count": 3,
                            "fu": 30,
                            "biao_dora_count": 1,
                            "yiman_zimo": False,
                            "count_zimo": 4,
                            "fu_zimo": 20,
                        }
                    ],
                    "already_hule": False,
                },
                {
                    "tingpai": False,
                    "hand": [],
                    "tings": [],
                    "already_hule": False,
                },
                {
                    "tingpai": True,
                    "hand": ["4s", "5s", "6s"],
                    "tings": [],
                    "already_hule": True,
                },
            ],
            "scores": [
                {
                    "seat": 2,
                    "old_scores": [35000, 35000, 35000],
                    "delta_scores": [-4000, -4000, 8000],
                    "hand": ["1z"] * 13,
                    "ming": ["kezi(2z,2z,2z)"],
                    "doras": ["3p"],
                    "score": 8000,
                    "taxes": [0, 0, 0],
                    "lines": ["liujumanguan"],
                }
            ],
            "gameend": True,
            "muyu": {"seat": 0},
            "hules_history": [{"seat": 1}],
        },
    )

    assert event == NoTileEvent(
        action_step=8,
        liujumanguan=True,
        players=(
            NoTilePlayer(
                tingpai=True,
                hand=(
                    validate_tile("1m"),
                    validate_tile("2m"),
                    validate_tile("3m"),
                ),
            ),
            NoTilePlayer(
                tingpai=False,
                hand=(),
            ),
            NoTilePlayer(
                tingpai=True,
                hand=(
                    validate_tile("4s"),
                    validate_tile("5s"),
                    validate_tile("6s"),
                ),
            ),
        ),
        scores=(
            NoTileScore(
                seat=validate_seat(2),
                old_scores=(35000, 35000, 35000),
                delta_scores=(-4000, -4000, 8000),
                hand=(validate_tile("1z"),) * 13,
                ming=("kezi(2z,2z,2z)",),
                dora_indicators=(validate_tile("3p"),),
                score=8000,
            ),
        ),
        game_end=True,
    )


@pytest.mark.parametrize("player_count", [0, 2, 5])
def test_no_tile_event_rejects_invalid_player_count(
    player_count: int,
) -> None:
    with pytest.raises(ValueError, match="three or four"):
        NoTileEvent.from_dict(
            8,
            {
                "liujumanguan": False,
                "players": [_player_data() for _ in range(player_count)],
                "scores": [],
                "gameend": False,
            },
        )


def test_no_tile_event_rejects_score_collection_length() -> None:
    with pytest.raises(ValueError, match="score collections"):
        NoTileEvent.from_dict(
            8,
            {
                "liujumanguan": True,
                "players": [_player_data() for _ in range(4)],
                "scores": [
                    {
                        **_score_data(seat=0),
                        "delta_scores": [0, 0, 0],
                    }
                ],
                "gameend": False,
            },
        )


def test_no_tile_event_rejects_duplicate_score_seats() -> None:
    with pytest.raises(ValueError, match="unique"):
        NoTileEvent.from_dict(
            8,
            {
                "liujumanguan": True,
                "players": [_player_data() for _ in range(4)],
                "scores": [
                    _score_data(seat=1, score=8000),
                    _score_data(seat=1, score=8000),
                ],
                "gameend": False,
            },
        )


def test_no_tile_score_uses_none_seat_without_liujumanguan() -> None:
    score = NoTileScore.from_dict(_score_data(seat=0))

    assert score.seat is None


def _player_data() -> dict[str, JsonValue]:
    return {
        "tingpai": False,
        "hand": [],
        "tings": [],
        "already_hule": False,
    }


def _score_data(*, seat: int, score: int = 0) -> dict[str, JsonValue]:
    return {
        "seat": seat,
        "old_scores": [25000] * 4,
        "delta_scores": [0] * 4,
        "hand": [],
        "ming": [],
        "doras": [],
        "score": score,
        "taxes": [],
        "lines": [],
    }
