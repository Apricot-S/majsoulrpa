import pytest

from majsoulrpa.screens.match import (
    Angang,
    Chi,
    Daminggang,
    DapaiEvent,
    Fulu,
    Jiagang,
    MatchEvent,
    Peng,
    ZimoEvent,
    validate_seat,
    validate_tile,
)
from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)
from majsoulrpa.screens.match.operation._materialize import (
    materialize_operation_candidates,
)
from majsoulrpa.screens.match.operation._specification import (
    _OperationCandidatesSpecification,
)


def _angang(tile: str) -> Angang:
    validated_tile = validate_tile(tile)
    return Angang(
        consumed=(
            validated_tile,
            validated_tile,
            validated_tile,
            validated_tile,
        )
    )


_FOUR_FULU = (
    _angang("1m"),
    _angang("2p"),
    _angang("3s"),
    _angang("4z"),
)


@pytest.mark.parametrize(
    ("operation_type", "combination", "event", "shoupai", "zimopai"),
    [
        (
            2,
            "3m|4m",
            DapaiEvent(
                action_step=1,
                seat=validate_seat(3),
                tile=validate_tile("5m"),
                moqie=False,
                liqi=False,
                wliqi=False,
                dora_indicators=(),
            ),
            ("3m", "4m"),
            None,
        ),
        (
            3,
            "5m|5m",
            DapaiEvent(
                action_step=1,
                seat=validate_seat(2),
                tile=validate_tile("5m"),
                moqie=False,
                liqi=False,
                wliqi=False,
                dora_indicators=(),
            ),
            ("5m", "5m"),
            None,
        ),
        (
            4,
            "1z|1z|1z|1z",
            ZimoEvent(
                action_step=1,
                seat=validate_seat(0),
                tile=validate_tile("1z"),
                left_tile_count=60,
                dora_indicators=(),
            ),
            ("1z", "1z", "1z"),
            "1z",
        ),
        (
            5,
            "5m|5m|5m",
            DapaiEvent(
                action_step=1,
                seat=validate_seat(2),
                tile=validate_tile("5m"),
                moqie=False,
                liqi=False,
                wliqi=False,
                dora_indicators=(),
            ),
            ("5m", "5m", "5m"),
            None,
        ),
    ],
)
def test_materialization_rejects_a_fifth_fulu(
    operation_type: int,
    combination: str,
    event: MatchEvent,
    shoupai: tuple[str, ...],
    zimopai: str | None,
) -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": operation_type,
                        "combination": [combination],
                    }
                ],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None

    with pytest.raises(ValueError, match="fifth fulu"):
        materialize_operation_candidates(
            specification,
            event,
            tuple(validate_tile(tile) for tile in shoupai),
            None if zimopai is None else validate_tile(zimopai),
            _FOUR_FULU,
            validate_seat(0),
            4,
        )


def _liqi_specification() -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["3p"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    return specification


def _liqi_event() -> ZimoEvent:
    return ZimoEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile("3p"),
        left_tile_count=60,
        dora_indicators=(),
    )


@pytest.mark.parametrize(
    "fulu",
    [
        Chi(
            from_seat=validate_seat(3),
            tile=validate_tile("3m"),
            consumed=(validate_tile("1m"), validate_tile("2m")),
        ),
        Peng(
            from_seat=validate_seat(2),
            tile=validate_tile("5p"),
            consumed=(validate_tile("5p"), validate_tile("5p")),
        ),
        Daminggang(
            from_seat=validate_seat(1),
            tile=validate_tile("7s"),
            consumed=(
                validate_tile("7s"),
                validate_tile("7s"),
                validate_tile("7s"),
            ),
        ),
        Jiagang(
            from_seat=validate_seat(1),
            tile=validate_tile("9m"),
            consumed=(validate_tile("9m"), validate_tile("9m")),
            added=validate_tile("9m"),
        ),
    ],
)
def test_liqi_materialization_rejects_open_fulu(fulu: Fulu) -> None:
    with pytest.raises(ValueError, match="closed hand"):
        materialize_operation_candidates(
            _liqi_specification(),
            _liqi_event(),
            (validate_tile("3p"),),
            validate_tile("3p"),
            (fulu,),
            validate_seat(0),
            4,
        )


def test_liqi_materialization_allows_angang() -> None:
    candidates = materialize_operation_candidates(
        _liqi_specification(),
        _liqi_event(),
        (validate_tile("3p"),),
        validate_tile("3p"),
        (_angang("1m"),),
        validate_seat(0),
        4,
    )

    assert candidates is not None
