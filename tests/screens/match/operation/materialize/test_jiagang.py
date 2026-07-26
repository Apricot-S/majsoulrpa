import pytest

from majsoulrpa.screens.match import (
    Angang,
    JiagangOperation,
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


def _peng(
    *,
    from_seat: int,
    tile: str,
    consumed: tuple[str, str],
) -> Peng:
    return Peng(
        from_seat=validate_seat(from_seat),
        tile=validate_tile(tile),
        consumed=(
            validate_tile(consumed[0]),
            validate_tile(consumed[1]),
        ),
    )


def _specification(
    *combinations: str,
) -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {"type": 6, "combination": list(combinations)}
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    return specification


def _zimo_event(tile: str = "9s") -> ZimoEvent:
    return ZimoEvent(
        action_step=2,
        seat=validate_seat(0),
        tile=validate_tile(tile),
        left_tile_count=60,
        dora_indicators=(),
    )


def test_jiagang_materialization_preserves_wire_candidate_order() -> None:
    peng_1m = _peng(from_seat=3, tile="1m", consumed=("1m", "1m"))
    peng_4p = _peng(from_seat=1, tile="4p", consumed=("4p", "4p"))
    peng_5p = _peng(from_seat=2, tile="5p", consumed=("5p", "5p"))

    candidates = materialize_operation_candidates(
        _specification(
            "4p|4p|4p|4p",
            "0p|5p|5p|5p",
            "1m|1m|1m|1m",
        ),
        _zimo_event(),
        (
            validate_tile("4p"),
            validate_tile("0p"),
            validate_tile("1m"),
        ),
        validate_tile("9s"),
        (peng_1m, peng_4p, peng_5p),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        JiagangOperation(
            from_seat=peng_4p.from_seat,
            tile=peng_4p.tile,
            consumed=peng_4p.consumed,
            added=validate_tile("4p"),
        ),
        JiagangOperation(
            from_seat=peng_5p.from_seat,
            tile=peng_5p.tile,
            consumed=peng_5p.consumed,
            added=validate_tile("0p"),
        ),
        JiagangOperation(
            from_seat=peng_1m.from_seat,
            tile=peng_1m.tile,
            consumed=peng_1m.consumed,
            added=validate_tile("1m"),
        ),
    )


def test_jiagang_materialization_identifies_normal_five_as_added() -> None:
    peng = _peng(from_seat=2, tile="0m", consumed=("5m", "5m"))

    candidates = materialize_operation_candidates(
        _specification("0m|5m|5m|5m"),
        _zimo_event("5m"),
        (),
        validate_tile("5m"),
        (peng,),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        JiagangOperation(
            from_seat=peng.from_seat,
            tile=peng.tile,
            consumed=peng.consumed,
            added=validate_tile("5m"),
        ),
    )


def test_liqi_flag_does_not_add_skip_to_jiagang() -> None:
    peng = _peng(from_seat=3, tile="1m", consumed=("1m", "1m"))

    candidates = materialize_operation_candidates(
        _specification("1m|1m|1m|1m"),
        _zimo_event(),
        (validate_tile("1m"),),
        validate_tile("9s"),
        (peng,),
        validate_seat(0),
        4,
        liqi=True,
    )

    assert candidates is not None
    assert candidates.operations == (
        JiagangOperation(
            from_seat=peng.from_seat,
            tile=peng.tile,
            consumed=peng.consumed,
            added=validate_tile("1m"),
        ),
    )


def test_jiagang_materialization_allows_replacing_one_of_four_fulu() -> None:
    peng = _peng(from_seat=2, tile="7z", consumed=("7z", "7z"))
    concealed_tile = validate_tile("1m")
    fulu = (
        Angang(
            consumed=(
                concealed_tile,
                concealed_tile,
                concealed_tile,
                concealed_tile,
            )
        ),
        _peng(from_seat=1, tile="2p", consumed=("2p", "2p")),
        peng,
        _peng(from_seat=3, tile="3s", consumed=("3s", "3s")),
    )

    candidates = materialize_operation_candidates(
        _specification("7z|7z|7z|7z"),
        _zimo_event("7z"),
        (),
        validate_tile("7z"),
        fulu,
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        JiagangOperation(
            from_seat=peng.from_seat,
            tile=peng.tile,
            consumed=peng.consumed,
            added=validate_tile("7z"),
        ),
    )


@pytest.mark.parametrize(
    ("fulu", "shoupai", "zimopai", "error_match"),
    [
        ((), ("5m",), "9s", "matching peng"),
        (
            (
                _peng(from_seat=1, tile="5m", consumed=("5m", "5m")),
                _peng(from_seat=2, tile="5m", consumed=("5m", "5m")),
            ),
            ("0m",),
            "9s",
            "matching peng",
        ),
        (
            (_peng(from_seat=1, tile="5m", consumed=("5m", "5m")),),
            ("1p",),
            "9s",
            "hand or drawn tile",
        ),
    ],
)
def test_jiagang_materialization_rejects_inconsistent_state(
    fulu: tuple[Peng, ...],
    shoupai: tuple[str, ...],
    zimopai: str,
    error_match: str,
) -> None:
    with pytest.raises(ValueError, match=error_match):
        materialize_operation_candidates(
            _specification("0m|5m|5m|5m"),
            _zimo_event(zimopai),
            tuple(validate_tile(tile) for tile in shoupai),
            validate_tile(zimopai),
            fulu,
            validate_seat(0),
            4,
        )


def test_jiagang_materialization_rejects_opponent_draw() -> None:
    event = ZimoEvent(
        action_step=2,
        seat=validate_seat(1),
        tile=None,
        left_tile_count=60,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="opponent draw"):
        materialize_operation_candidates(
            _specification("7z|7z|7z|7z"),
            event,
            (),
            None,
            (_peng(from_seat=2, tile="7z", consumed=("7z", "7z")),),
            validate_seat(0),
            4,
        )
