import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)
from majsoulrpa.screens.match.operation._specification import (
    _AngangOperationSpecification,
    _BabeiOperationSpecification,
    _ChiOperationSpecification,
    _DaminggangOperationSpecification,
    _DapaiOperationSpecification,
    _JiagangOperationSpecification,
    _LiqiOperationSpecification,
    _PengOperationSpecification,
)


def test_decode_dapai_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "seat": 0,
                "operation_list": [
                    {
                        "type": 1,
                        "combination": ["5m", "7z"],
                        "change_tiles": [],
                        "change_tile_states": [],
                        "gap_type": 0,
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    assert specification.time_fixed_ms == 5000
    assert specification.time_add_ms == 20000
    [operation] = specification.operations
    assert isinstance(operation, _DapaiOperationSpecification)
    assert operation.forbidden_tiles == ("5m", "7z")


def test_decode_chi_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 2,
                        "combination": ["1m|2m", "2m|4m"],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _ChiOperationSpecification)
    assert operation.consumed_candidates == (
        ("1m", "2m"),
        ("2m", "4m"),
    )


@pytest.mark.parametrize(
    "combination",
    [[], ["1m"], ["1m|2m|3m"], ["1m|1x"]],
)
def test_decode_chi_operation_rejects_invalid_combinations(
    combination: list[str],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [
                        {"type": 2, "combination": combination}
                    ],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


def test_decode_peng_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 3,
                        "combination": ["0m|5m", "5m|5m"],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _PengOperationSpecification)
    assert operation.consumed_candidates == (
        ("0m", "5m"),
        ("5m", "5m"),
    )


@pytest.mark.parametrize(
    "combination",
    [[], ["5m"], ["5m|5m|5m"], ["5m|5x"]],
)
def test_decode_peng_operation_rejects_invalid_combinations(
    combination: list[str],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [
                        {"type": 3, "combination": combination}
                    ],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


def test_decode_daminggang_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 5,
                        "combination": ["0m|5m|5m", "5m|5m|5m"],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _DaminggangOperationSpecification)
    assert operation.consumed_candidates == (
        ("0m", "5m", "5m"),
        ("5m", "5m", "5m"),
    )


def test_decode_angang_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 4,
                        "combination": [
                            "0m|5m|5m|5m",
                            "7z|7z|7z|7z",
                        ],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _AngangOperationSpecification)
    assert operation.consumed_candidates == (
        ("0m", "5m", "5m", "5m"),
        ("7z", "7z", "7z", "7z"),
    )


@pytest.mark.parametrize(
    "combination",
    [[], ["5m|5m|5m"], ["5m|5m|5m|5m|5m"], ["5m|5m|5m|5x"]],
)
def test_decode_angang_operation_rejects_invalid_combinations(
    combination: list[str],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [
                        {"type": 4, "combination": combination}
                    ],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


def test_decode_jiagang_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 6,
                        "combination": [
                            "0m|5m|5m|5m",
                            "7z|7z|7z|7z",
                        ],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _JiagangOperationSpecification)
    assert operation.tile_candidates == (
        ("0m", "5m", "5m", "5m"),
        ("7z", "7z", "7z", "7z"),
    )


@pytest.mark.parametrize(
    "combination",
    [[], ["5m|5m|5m"], ["5m|5m|5m|5m|5m"], ["5m|5m|5m|5x"]],
)
def test_decode_jiagang_operation_rejects_invalid_combinations(
    combination: list[str],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [
                        {"type": 6, "combination": combination}
                    ],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


@pytest.mark.parametrize(
    "combination",
    [[], ["5m|5m"], ["5m|5m|5m|5m"], ["5m|5m|5x"]],
)
def test_decode_daminggang_operation_rejects_invalid_combinations(
    combination: list[str],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [
                        {"type": 5, "combination": combination}
                    ],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


def test_decode_liqi_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 7,
                        "combination": ["0m", "3p"],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _LiqiOperationSpecification)
    assert operation.candidate_tiles == ("0m", "3p")


@pytest.mark.parametrize("combination", [[], ["1x"], ["1m|2m"]])
def test_decode_liqi_operation_rejects_invalid_combinations(
    combination: list[str],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [
                        {"type": 7, "combination": combination}
                    ],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


def test_decode_babei_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 11, "combination": []}],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    [operation] = specification.operations
    assert isinstance(operation, _BabeiOperationSpecification)


def test_decode_babei_operation_rejects_nonempty_combination() -> None:
    with pytest.raises(ValueError, match="must not contain"):
        decode_operation_specification(
            {
                "operation": {
                    "operation_list": [{"type": 11, "combination": ["4z"]}],
                    "time_add": 0,
                    "time_fixed": 0,
                }
            }
        )


@pytest.mark.parametrize(
    "data",
    [
        {},
        {
            "operation": {
                "operation_list": [],
                "time_add": 0,
                "time_fixed": 0,
            }
        },
    ],
)
def test_decode_absent_or_empty_operation_as_none(
    data: dict[str, JsonValue],
) -> None:
    assert decode_operation_specification(data) is None


@pytest.mark.parametrize(
    "operation",
    [
        [],
        {"operation_list": [], "time_add": True, "time_fixed": 0},
        {"operation_list": [], "time_add": 0, "time_fixed": -1},
        {"operation_list": {}, "time_add": 0, "time_fixed": 0},
        {
            "operation_list": [{"type": True, "combination": []}],
            "time_add": 0,
            "time_fixed": 0,
        },
        {
            "operation_list": [{"type": 1, "combination": ["1x"]}],
            "time_add": 0,
            "time_fixed": 0,
        },
        {
            "operation_list": [{"type": 99, "combination": []}],
            "time_add": 0,
            "time_fixed": 0,
        },
    ],
)
def test_decode_operation_rejects_invalid_or_unsupported_fields(
    operation: JsonValue,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification({"operation": operation})
