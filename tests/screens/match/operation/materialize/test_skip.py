from majsoulrpa.screens.match import (
    DapaiEvent,
    DapaiOperation,
    RongOperation,
    SkipOperation,
    ZimoEvent,
    ZimohuOperation,
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


def test_call_candidates_include_one_trailing_skip() -> None:
    candidates = materialize_operation_candidates(
        _specification(
            {"type": 3, "combination": ["5m|5m"]},
            {"type": 9, "combination": []},
        ),
        _dapai_event(),
        tuple(validate_tile(tile) for tile in ("5m", "5m", *["1p"] * 11)),
        None,
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert isinstance(candidates.operations[-2], RongOperation)
    assert candidates.operations[-1] == SkipOperation()
    assert candidates.operations.count(SkipOperation()) == 1


def test_non_liqi_self_draw_candidates_do_not_include_skip() -> None:
    candidates = materialize_operation_candidates(
        _specification(
            {"type": 1, "combination": []},
            {"type": 8, "combination": []},
        ),
        _zimo_event(),
        tuple(validate_tile("1m") for _ in range(13)),
        validate_tile("9s"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert any(
        isinstance(item, DapaiOperation) for item in candidates.operations
    )
    assert any(
        isinstance(item, ZimohuOperation) for item in candidates.operations
    )
    assert SkipOperation() not in candidates.operations


def test_liqi_self_draw_candidates_include_trailing_skip() -> None:
    candidates = materialize_operation_candidates(
        _specification({"type": 8, "combination": []}),
        _zimo_event(),
        tuple(validate_tile("1m") for _ in range(13)),
        validate_tile("9s"),
        (),
        validate_seat(0),
        4,
        liqi=True,
    )

    assert candidates is not None
    assert candidates.operations == (
        ZimohuOperation(tile=validate_tile("9s")),
        SkipOperation(),
    )


def _specification(
    *operations: dict[str, object],
) -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": list(operations),
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    return specification


def _dapai_event() -> DapaiEvent:
    return DapaiEvent(
        action_step=1,
        seat=validate_seat(3),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )


def _zimo_event() -> ZimoEvent:
    return ZimoEvent(
        action_step=2,
        seat=validate_seat(0),
        tile=validate_tile("9s"),
        left_tile_count=68,
        dora_indicators=(),
    )
