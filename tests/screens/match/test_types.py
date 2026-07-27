import pytest

from majsoulrpa.screens.match import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


def test_validate_seat_returns_seat() -> None:
    seat: Seat = validate_seat(3)

    assert seat == 3


@pytest.mark.parametrize("value", [True, -1, 4])
def test_validate_seat_rejects_invalid_value(value: int) -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_seat(value)


@pytest.mark.parametrize("value", ["0m", "5p", "9s", "7z"])
def test_validate_tile_returns_tile(value: str) -> None:
    tile: Tile = validate_tile(value)

    assert tile == value


@pytest.mark.parametrize("value", ["", "10m", "0z", "8z", "1x"])
def test_validate_tile_rejects_invalid_value(value: str) -> None:
    with pytest.raises(ValueError, match="Invalid tile"):
        validate_tile(value)
