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
