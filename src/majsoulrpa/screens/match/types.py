from typing import NewType

Seat = NewType("Seat", int)
Tile = NewType("Tile", str)

_MAX_SEAT = 3
_TILE_LENGTH = 2


def validate_seat(value: int) -> Seat:
    if isinstance(value, bool):
        msg = "Seat must be an int."
        raise TypeError(msg)
    if not 0 <= value <= _MAX_SEAT:
        msg = "Seat must be between 0 and 3."
        raise ValueError(msg)
    return Seat(value)


def validate_tile(value: str) -> Tile:
    if len(value) != _TILE_LENGTH:
        msg = f"Invalid tile: {value!r}."
        raise ValueError(msg)
    number = value[0]
    suit = value[1]
    if suit in {"m", "p", "s"} and number in "0123456789":
        return Tile(value)
    if suit == "z" and number in "1234567":
        return Tile(value)
    msg = f"Invalid tile: {value!r}."
    raise ValueError(msg)
