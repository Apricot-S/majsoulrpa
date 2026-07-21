from dataclasses import FrozenInstanceError

import pytest

from majsoulrpa.screens.match import (
    DapaiOperation,
    OperationCandidates,
    validate_tile,
)


def test_dapai_operation_is_an_immutable_value() -> None:
    operation = DapaiOperation(tile=validate_tile("0m"), moqie=True)

    assert operation.tile == "0m"
    assert operation.moqie is True
    with pytest.raises(FrozenInstanceError):
        operation.moqie = False  # ty: ignore[invalid-assignment]


def test_operation_candidates_is_an_immutable_value() -> None:
    operation = DapaiOperation(tile=validate_tile("1m"), moqie=False)
    candidates = OperationCandidates(
        time_fixed_ms=5000,
        time_add_ms=20000,
        operations=(operation,),
    )

    assert candidates.operations == (operation,)
    with pytest.raises(FrozenInstanceError):
        candidates.operations = ()  # ty: ignore[invalid-assignment]


@pytest.mark.parametrize(
    ("time_fixed_ms", "time_add_ms", "operations", "error_match"),
    [
        (
            -1,
            0,
            (DapaiOperation(tile=validate_tile("1m"), moqie=False),),
            "nonnegative",
        ),
        (
            0,
            -1,
            (DapaiOperation(tile=validate_tile("1m"), moqie=False),),
            "nonnegative",
        ),
        (0, 0, (), "must not be empty"),
    ],
)
def test_operation_candidates_rejects_invalid_values(
    time_fixed_ms: int,
    time_add_ms: int,
    operations: tuple[DapaiOperation, ...],
    error_match: str,
) -> None:
    with pytest.raises(ValueError, match=error_match):
        OperationCandidates(
            time_fixed_ms=time_fixed_ms,
            time_add_ms=time_add_ms,
            operations=operations,
        )
