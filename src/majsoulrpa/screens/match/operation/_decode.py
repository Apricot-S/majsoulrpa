from collections.abc import Mapping

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_int,
    _get_optional_dict,
    _get_str_list,
)
from majsoulrpa.screens.match.operation._specification import (
    _AngangOperationSpecification,
    _ChiOperationSpecification,
    _DaminggangOperationSpecification,
    _DapaiOperationSpecification,
    _JiagangOperationSpecification,
    _LiqiOperationSpecification,
    _MatchOperationSpecification,
    _OperationCandidatesSpecification,
    _PengOperationSpecification,
)
from majsoulrpa.screens.match.types import Tile, validate_tile

_TWO_TILE_COMBINATION_COUNT = 2
_THREE_TILE_COMBINATION_COUNT = 3
_FOUR_TILE_COMBINATION_COUNT = 4


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
        match operation_type:
            case 1:
                specification = _decode_dapai_specification(item)
            case 2:
                specification = _decode_chi_specification(item)
            case 3:
                specification = _decode_peng_specification(item)
            case 4:
                specification = _decode_angang_specification(item)
            case 5:
                specification = _decode_daminggang_specification(item)
            case 6:
                specification = _decode_jiagang_specification(item)
            case 7:
                specification = _decode_liqi_specification(item)
            case _:
                msg = (
                    "OptionalOperation type is not supported: "
                    f"{operation_type}."
                )
                raise ValueError(msg)
        specifications.append(specification)

    if not specifications:
        return None
    return _OperationCandidatesSpecification(
        time_fixed_ms=time_fixed_ms,
        time_add_ms=time_add_ms,
        operations=tuple(specifications),
    )


def _decode_dapai_specification(
    item: Mapping[str, JsonValue],
) -> _DapaiOperationSpecification:
    return _DapaiOperationSpecification(
        forbidden_tiles=tuple(
            validate_tile(tile)
            for tile in _get_str_list(item, "OptionalOperation.combination")
        ),
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


def _decode_daminggang_specification(
    item: Mapping[str, JsonValue],
) -> _DaminggangOperationSpecification:
    encoded_combinations = _get_str_list(item, "OptionalOperation.combination")
    if not encoded_combinations:
        msg = "A daminggang operation must contain a combination."
        raise ValueError(msg)

    consumed_candidates: list[tuple[Tile, Tile, Tile]] = []
    for encoded_combination in encoded_combinations:
        tiles = encoded_combination.split("|")
        if len(tiles) != _THREE_TILE_COMBINATION_COUNT:
            msg = "A daminggang combination must contain three tiles."
            raise ValueError(msg)
        consumed_candidates.append(
            (
                validate_tile(tiles[0]),
                validate_tile(tiles[1]),
                validate_tile(tiles[2]),
            )
        )
    return _DaminggangOperationSpecification(
        consumed_candidates=tuple(consumed_candidates)
    )


def _decode_angang_specification(
    item: Mapping[str, JsonValue],
) -> _AngangOperationSpecification:
    return _AngangOperationSpecification(
        consumed_candidates=_decode_four_tile_combinations(item, "angang")
    )


def _decode_jiagang_specification(
    item: Mapping[str, JsonValue],
) -> _JiagangOperationSpecification:
    return _JiagangOperationSpecification(
        tile_candidates=_decode_four_tile_combinations(item, "jiagang")
    )


def _decode_liqi_specification(
    item: Mapping[str, JsonValue],
) -> _LiqiOperationSpecification:
    candidate_tiles = tuple(
        validate_tile(tile)
        for tile in _get_str_list(item, "OptionalOperation.combination")
    )
    if not candidate_tiles:
        msg = "A liqi operation must contain a candidate tile."
        raise ValueError(msg)
    return _LiqiOperationSpecification(candidate_tiles=candidate_tiles)


def _decode_four_tile_combinations(
    item: Mapping[str, JsonValue],
    operation_name: str,
) -> tuple[tuple[Tile, Tile, Tile, Tile], ...]:
    subject = (
        f"An {operation_name}"
        if operation_name[0] in {"a", "e", "i", "o", "u"}
        else f"A {operation_name}"
    )
    encoded_combinations = _get_str_list(item, "OptionalOperation.combination")
    if not encoded_combinations:
        msg = f"{subject} operation must contain a combination."
        raise ValueError(msg)

    candidates: list[tuple[Tile, Tile, Tile, Tile]] = []
    for encoded_combination in encoded_combinations:
        tiles = encoded_combination.split("|")
        if len(tiles) != _FOUR_TILE_COMBINATION_COUNT:
            msg = f"{subject} combination must contain four tiles."
            raise ValueError(msg)
        candidates.append(
            (
                validate_tile(tiles[0]),
                validate_tile(tiles[1]),
                validate_tile(tiles[2]),
                validate_tile(tiles[3]),
            )
        )
    return tuple(candidates)


def _decode_two_tile_combinations(
    item: Mapping[str, JsonValue],
    operation_name: str,
) -> tuple[tuple[Tile, Tile], ...]:
    encoded_combinations = _get_str_list(item, "OptionalOperation.combination")
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
