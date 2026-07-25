import pytest

from majsoulrpa.screens.match import (
    AngangEvent,
    BabeiEvent,
    DapaiEvent,
    JiagangEvent,
    MatchEvent,
    RongOperation,
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


def _specification() -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 9, "combination": []}],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    return specification


@pytest.mark.parametrize(
    ("event", "player_count", "from_seat", "tile"),
    [
        (
            DapaiEvent(
                action_step=1,
                seat=validate_seat(2),
                tile=validate_tile("0m"),
                moqie=False,
                liqi=False,
                wliqi=False,
                dora_indicators=(),
            ),
            4,
            2,
            "0m",
        ),
        (
            AngangEvent(
                action_step=2,
                seat=validate_seat(2),
                consumed=(
                    validate_tile("0p"),
                    validate_tile("5p"),
                    validate_tile("5p"),
                    validate_tile("5p"),
                ),
                dora_indicators=(),
            ),
            4,
            2,
            "0p",
        ),
        (
            JiagangEvent(
                action_step=2,
                seat=validate_seat(1),
                consumed=(
                    validate_tile("5s"),
                    validate_tile("5s"),
                    validate_tile("5s"),
                ),
                added=validate_tile("0s"),
                dora_indicators=(),
            ),
            4,
            1,
            "0s",
        ),
        (
            BabeiEvent(
                action_step=2,
                seat=validate_seat(2),
                moqie=True,
                dora_indicators=(),
            ),
            3,
            2,
            "4z",
        ),
    ],
)
def test_rong_materialization_uses_event_action_target(
    event: MatchEvent,
    player_count: int,
    from_seat: int,
    tile: str,
) -> None:
    candidates = materialize_operation_candidates(
        _specification(),
        event,
        tuple(validate_tile("1m") for _ in range(13)),
        None,
        (),
        validate_seat(0),
        player_count,
    )

    assert candidates is not None
    assert candidates.operations == (
        RongOperation(
            from_seat=validate_seat(from_seat),
            tile=validate_tile(tile),
        ),
    )


def test_rong_materialization_rejects_self_action_target() -> None:
    event = DapaiEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="self player"):
        materialize_operation_candidates(
            _specification(),
            event,
            tuple(validate_tile("1m") for _ in range(13)),
            None,
            (),
            validate_seat(0),
            4,
        )


def test_rong_materialization_rejects_unrelated_event() -> None:
    event = ZimoEvent(
        action_step=2,
        seat=validate_seat(1),
        tile=None,
        left_tile_count=68,
        dora_indicators=(),
    )

    with pytest.raises(TypeError, match="action target"):
        materialize_operation_candidates(
            _specification(),
            event,
            tuple(validate_tile("1m") for _ in range(13)),
            None,
            (),
            validate_seat(0),
            4,
        )


def test_rong_materialization_rejects_unresolved_self_draw() -> None:
    event = DapaiEvent(
        action_step=1,
        seat=validate_seat(2),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="unresolved draw"):
        materialize_operation_candidates(
            _specification(),
            event,
            tuple(validate_tile("1m") for _ in range(13)),
            validate_tile("1p"),
            (),
            validate_seat(0),
            4,
        )
