import pytest

from majsoulrpa.screens.match import (
    Hule,
    HuleEvent,
    HuleFan,
    validate_seat,
    validate_tile,
)


def test_hule_event_from_dict() -> None:
    event = HuleEvent.from_dict(
        3,
        {
            "hules": [
                {
                    "hand": ["1m", "2m", "3m"],
                    "ming": ["kezi(4p,4p,4p)"],
                    "hu_tile": "0s",
                    "seat": 0,
                    "zimo": True,
                    "qinjia": False,
                    "liqi": True,
                    "doras": ["0s"],
                    "li_doras": ["4z"],
                    "yiman": False,
                    "count": 3,
                    "fans": [{"name": "立直", "val": 1, "id": 2}],
                    "fu": 30,
                    "title": "",
                    "point_rong": 0,
                    "point_zimo_qin": 2000,
                    "point_zimo_xian": 1000,
                    "title_id": 0,
                    "point_sum": 4000,
                    "dadian": 4000,
                    "baopai": 2,
                    "baopai_seats": [2, 3],
                },
            ],
            "old_scores": [25000, 25000, 25000, 25000],
            "delta_scores": [4300, -2100, -1100, -1100],
            "scores": [29300, 22900, 23900, 23900],
            "doras": ["3p"],
            "gameend": {"scores": [29300, 22900, 23900, 23900]},
            "baopai": 3,
        },
    )

    assert event == HuleEvent(
        action_step=3,
        hules=(
            Hule(
                hand=(
                    validate_tile("1m"),
                    validate_tile("2m"),
                    validate_tile("3m"),
                ),
                ming=("kezi(4p,4p,4p)",),
                hu_tile=validate_tile("0s"),
                seat=validate_seat(0),
                zimo=True,
                qinjia=False,
                liqi=True,
                dora_indicators=(validate_tile("0s"),),
                li_dora_indicators=(validate_tile("4z"),),
                yiman=False,
                count=3,
                fans=(HuleFan(name="立直", value=1, id=2),),
                fu=30,
                title="",
                point_rong=0,
                point_zimo_qin=2000,
                point_zimo_xian=1000,
                title_id=0,
                point_sum=4000,
                dadian=4000,
                baopai_seat=validate_seat(1),
                baopai_seats=(validate_seat(2), validate_seat(3)),
            ),
        ),
        old_scores=(25000, 25000, 25000, 25000),
        delta_scores=(4300, -2100, -1100, -1100),
        scores=(29300, 22900, 23900, 23900),
        dora_indicators=(validate_tile("3p"),),
        game_end_scores=(29300, 22900, 23900, 23900),
        baopai_seat=validate_seat(2),
    )


def test_hule_event_preserves_multiple_hules_in_message_order() -> None:
    event = HuleEvent.from_dict(
        5,
        {
            "hules": [
                _hule_data(seat=2, tile="5m"),
                _hule_data(seat=1, tile="5m"),
            ],
            "old_scores": [25000] * 4,
            "delta_scores": [0] * 4,
            "scores": [25000] * 4,
            "doras": ["3p"],
            "gameend": None,
            "baopai": 0,
        },
    )

    assert tuple(hule.seat for hule in event.hules) == (2, 1)


def test_hule_event_rejects_inconsistent_score_lengths() -> None:
    with pytest.raises(ValueError, match="score collections"):
        HuleEvent.from_dict(
            3,
            {
                "hules": [_hule_data(seat=0, tile="1m", zimo=True)],
                "old_scores": [25000] * 4,
                "delta_scores": [0] * 3,
                "scores": [25000] * 4,
                "doras": ["3p"],
                "gameend": None,
                "baopai": 0,
            },
        )


def test_hule_event_accepts_disabled_dora() -> None:
    event = HuleEvent.from_dict(
        3,
        {
            "hules": [_hule_data(seat=0, tile="1m", zimo=True)],
            "old_scores": [25000] * 4,
            "delta_scores": [0] * 4,
            "scores": [25000] * 4,
            "doras": [],
            "gameend": None,
            "baopai": 0,
        },
    )

    assert event.dora_indicators == ()
    assert event.baopai_seat is None
    assert event.hules[0].baopai_seat is None


@pytest.mark.parametrize("baopai", [-1, 5])
def test_hule_event_rejects_invalid_legacy_baopai(baopai: int) -> None:
    data = _hule_data(seat=0, tile="1m", zimo=True)
    data["baopai"] = baopai

    with pytest.raises(ValueError, match="baopai"):
        HuleEvent.from_dict(
            3,
            {
                "hules": [data],
                "old_scores": [25000] * 4,
                "delta_scores": [0] * 4,
                "scores": [25000] * 4,
                "doras": [],
                "gameend": None,
                "baopai": 0,
            },
        )


def _hule_data(
    *,
    seat: int,
    tile: str,
    zimo: bool = False,
) -> dict[str, object]:
    return {
        "hand": ["1m"] * 13,
        "ming": [],
        "hu_tile": tile,
        "seat": seat,
        "zimo": zimo,
        "qinjia": False,
        "liqi": False,
        "doras": [],
        "li_doras": [],
        "yiman": False,
        "count": 0,
        "fans": [],
        "fu": 30,
        "title": "",
        "point_rong": 0,
        "point_zimo_qin": 0,
        "point_zimo_xian": 0,
        "title_id": 0,
        "point_sum": 0,
        "dadian": 0,
        "baopai": 0,
        "baopai_seats": [],
    }
