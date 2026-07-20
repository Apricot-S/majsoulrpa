from majsoulrpa.screens.match.types import Tile

_SUIT_ORDER = {"m": 0, "p": 1, "s": 2, "z": 3}


def tile_sort_key(tile: Tile) -> tuple[int, int, int]:
    number = int(tile[0])
    suit = tile[1]
    if number == 0:
        number = 5
        red_order = 0
    else:
        red_order = 1
    return _SUIT_ORDER[suit], number, red_order
