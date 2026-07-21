from majsoulrpa.screens.match.types import Tile


def validate_chi_tiles(tile: Tile, consumed: tuple[Tile, Tile]) -> None:
    tiles = (*consumed, tile)
    suits = {value[1] for value in tiles}
    numbers = sorted(
        5 if value[0] == "0" else int(value[0]) for value in tiles
    )
    if (
        len(suits) != 1
        or not suits <= {"m", "p", "s"}
        or numbers != list(range(numbers[0], numbers[0] + 3))
    ):
        msg = "tiles must form a suited sequence."
        raise ValueError(msg)


def validate_same_tile_kind(tile: Tile, consumed: tuple[Tile, ...]) -> None:
    expected = _normalized_tile_kind(tile)
    if any(_normalized_tile_kind(value) != expected for value in consumed):
        msg = "tiles must have the same kind."
        raise ValueError(msg)


def _normalized_tile_kind(tile: Tile) -> str:
    if tile[0] == "0":
        return f"5{tile[1]}"
    return tile
