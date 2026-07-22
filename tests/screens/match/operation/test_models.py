from dataclasses import FrozenInstanceError

import pytest

from majsoulrpa.screens.match import (
    ChiOperation,
    DapaiOperation,
    LiqiOperation,
    OperationCandidates,
    PengOperation,
    validate_seat,
    validate_tile,
)


def test_dapai_operation_is_an_immutable_value() -> None:
    operation = DapaiOperation(tile=validate_tile("0m"), moqie=True)

    assert operation.tile == "0m"
    assert operation.moqie is True
    with pytest.raises(FrozenInstanceError):
        operation.moqie = False  # ty: ignore[invalid-assignment]


def test_liqi_operation_is_an_immutable_value() -> None:
    operation = LiqiOperation(tile=validate_tile("0m"), moqie=True)

    assert operation.tile == "0m"
    assert operation.moqie is True
    with pytest.raises(FrozenInstanceError):
        operation.moqie = False  # ty: ignore[invalid-assignment]


def test_chi_operation_is_an_immutable_value() -> None:
    operation = ChiOperation(
        from_seat=validate_seat(3),
        tile=validate_tile("5m"),
        consumed=(validate_tile("3m"), validate_tile("4m")),
    )

    assert operation.from_seat == 3
    assert operation.tile == "5m"
    assert operation.consumed == ("3m", "4m")
    with pytest.raises(FrozenInstanceError):
        operation.tile = validate_tile("6m")  # ty: ignore[invalid-assignment]


def test_chi_operation_rejects_tiles_that_do_not_form_a_sequence() -> None:
    with pytest.raises(ValueError, match="sequence"):
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("5m"),
            consumed=(validate_tile("2m"), validate_tile("3m")),
        )


def test_peng_operation_is_an_immutable_value() -> None:
    operation = PengOperation(
        from_seat=validate_seat(2),
        tile=validate_tile("5m"),
        consumed=(validate_tile("0m"), validate_tile("5m")),
    )

    assert operation.from_seat == 2
    assert operation.tile == "5m"
    assert operation.consumed == ("0m", "5m")
    with pytest.raises(FrozenInstanceError):
        operation.tile = validate_tile("6m")  # ty: ignore[invalid-assignment]


def test_peng_operation_rejects_tiles_of_different_kinds() -> None:
    with pytest.raises(ValueError, match="same kind"):
        PengOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("5m"), validate_tile("5p")),
        )


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
