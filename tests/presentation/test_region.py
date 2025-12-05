import pytest

from majsoulrpa.presentation.region import Region


def test_region_boundary_values() -> None:
    region = Region(0.0, 0.0, 1.0, 1.0)
    assert region.left == 0
    assert region.top == 0
    assert region.width == 1
    assert region.height == 1


@pytest.mark.parametrize(
    ("left", "top", "width", "height"),
    [
        (-0.1, 0.0, 1.0, 1.0),
        (0, -1.0, 1.0, 1.0),
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
    ],
)
def test_region_invalid_values(
    left: float,
    top: float,
    width: float,
    height: float,
) -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        Region(left, top, width, height)
