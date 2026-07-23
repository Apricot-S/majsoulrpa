from majsoulrpa.screens.match.types import Seat, Tile


def is_preceding_seat(
    seat: Seat,
    *,
    relative_to: Seat,
    player_count: int,
) -> bool:
    return seat == (relative_to - 1) % player_count


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
    expected = normalize_tile_kind(tile)
    if any(normalize_tile_kind(value) != expected for value in consumed):
        msg = "tiles must have the same kind."
        raise ValueError(msg)


def normalize_tile_kind(tile: Tile) -> Tile:
    if tile[0] == "0":
        return Tile(f"5{tile[1]}")
    return tile
