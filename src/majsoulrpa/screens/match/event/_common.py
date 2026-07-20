_SUIT_ORDER = {"m": 0, "p": 1, "s": 2, "z": 3}
_TILE_LENGTH = 2


def validate_tile(tile: str) -> None:
    number = tile[0] if len(tile) == _TILE_LENGTH else ""
    suit = tile[1] if len(tile) == _TILE_LENGTH else ""
    if suit in {"m", "p", "s"} and number in "0123456789":
        return
    if suit == "z" and number in "1234567":
        return
    msg = f"Invalid tile: {tile!r}."
    raise ValueError(msg)


def tile_sort_key(tile: str) -> tuple[int, int, int]:
    validate_tile(tile)
    number = int(tile[0])
    suit = tile[1]
    if number == 0:
        number = 5
        red_order = 0
    else:
        red_order = 1
    return _SUIT_ORDER[suit], number, red_order
