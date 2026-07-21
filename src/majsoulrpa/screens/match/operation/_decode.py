from collections.abc import Mapping

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_int,
    _get_optional_dict,
    _get_str_list,
)
from majsoulrpa.screens.match.operation._specification import (
    _ChiOperationSpecification,
    _DapaiOperationSpecification,
    _MatchOperationSpecification,
    _OperationCandidatesSpecification,
    _PengOperationSpecification,
)
from majsoulrpa.screens.match.types import Tile, validate_tile

_DAPAI_OPERATION_TYPE = 1
_CHI_OPERATION_TYPE = 2
_PENG_OPERATION_TYPE = 3

_TWO_TILE_COMBINATION_COUNT = 2


def decode_operation_specification(
    data: Mapping[str, JsonValue],
) -> _OperationCandidatesSpecification | None:
    operation = _get_optional_dict(data, "operation")
    if operation is None:
        return None

    time_fixed_ms = _get_int(operation, "OptionalOperationList.time_fixed")
    time_add_ms = _get_int(operation, "OptionalOperationList.time_add")
    if time_fixed_ms < 0 or time_add_ms < 0:
        msg = "OptionalOperationList time must be nonnegative."
        raise ValueError(msg)

    operation_list = operation.get("operation_list")
    if not isinstance(operation_list, list):
        msg = "OptionalOperationList.operation_list must be a list."
        raise TypeError(msg)

    specifications: list[_MatchOperationSpecification] = []
    for item in operation_list:
        if not isinstance(item, dict):
            msg = "OptionalOperationList.operation_list items must be objects."
            raise TypeError(msg)
        operation_type = _get_int(item, "OptionalOperation.type")
        if operation_type == _DAPAI_OPERATION_TYPE:
            specifications.append(
                _DapaiOperationSpecification(
                    forbidden_tiles=tuple(
                        validate_tile(tile)
                        for tile in _get_str_list(
                            item,
                            "OptionalOperation.combination",
                        )
                    ),
                )
            )
            continue
        if operation_type == _CHI_OPERATION_TYPE:
            specifications.append(_decode_chi_specification(item))
            continue
        if operation_type == _PENG_OPERATION_TYPE:
            specifications.append(_decode_peng_specification(item))
            continue
        msg = f"OptionalOperation type is not supported: {operation_type}."
        raise ValueError(msg)

    if not specifications:
        return None
    return _OperationCandidatesSpecification(
        time_fixed_ms=time_fixed_ms,
        time_add_ms=time_add_ms,
        operations=tuple(specifications),
    )


def _decode_chi_specification(
    item: Mapping[str, JsonValue],
) -> _ChiOperationSpecification:
    return _ChiOperationSpecification(
        consumed_candidates=_decode_two_tile_combinations(item, "chi"),
    )


def _decode_peng_specification(
    item: Mapping[str, JsonValue],
) -> _PengOperationSpecification:
    return _PengOperationSpecification(
        consumed_candidates=_decode_two_tile_combinations(item, "peng"),
    )


def _decode_two_tile_combinations(
    item: Mapping[str, JsonValue],
    operation_name: str,
) -> tuple[tuple[Tile, Tile], ...]:
    encoded_combinations = _get_str_list(
        item,
        "OptionalOperation.combination",
    )
    if not encoded_combinations:
        msg = f"A {operation_name} operation must contain a combination."
        raise ValueError(msg)

    consumed_candidates: list[tuple[Tile, Tile]] = []
    for encoded_combination in encoded_combinations:
        tiles = encoded_combination.split("|")
        if len(tiles) != _TWO_TILE_COMBINATION_COUNT:
            msg = f"A {operation_name} combination must contain two tiles."
            raise ValueError(msg)
        consumed_candidates.append(
            (validate_tile(tiles[0]), validate_tile(tiles[1]))
        )
    return tuple(consumed_candidates)
