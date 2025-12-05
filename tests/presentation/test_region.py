import pytest

from majsoulrpa.presentation.region import Region


def test_region_boundary_values() -> None:
    region = Region(0.0, 0.0, 1.0, 1.0)
    assert region.left == 0.0
    assert region.top == 0.0
    assert region.width == 1.0
    assert region.height == 1.0


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


@pytest.mark.parametrize(
    ("scale", "left", "top", "width", "height"),
    [
        (1.0, 0.0, 0.0, 1.0, 2.0),
        (2.0, 0.0, 0.0, 2.0, 4.0),
        (0.5, 0.0, 0.0, 0.5, 1.0),
    ],
)
def test_scale_origin(
    scale: float,
    left: float,
    top: float,
    width: float,
    height: float,
) -> None:
    base = Region(0.0, 0.0, 1.0, 2.0)
    scaled = base.scale(scale)
    assert pytest.approx(scaled.left, rel=1e-9) == left
    assert pytest.approx(scaled.top, rel=1e-9) == top
    assert pytest.approx(scaled.width, rel=1e-9) == width
    assert pytest.approx(scaled.height, rel=1e-9) == height


@pytest.mark.parametrize(
    ("scale", "left", "top", "width", "height"),
    [
        (1.0, 1.0, 2.0, 3.0, 4.0),
        (2.0, 2.0, 4.0, 6.0, 8.0),
        (0.5, 0.5, 1.0, 1.5, 2.0),
    ],
)
def test_scale_non_origin(
    scale: float,
    left: float,
    top: float,
    width: float,
    height: float,
) -> None:
    base = Region(1.0, 2.0, 3.0, 4.0)
    scaled = base.scale(scale)
    assert pytest.approx(scaled.left, rel=1e-9) == left
    assert pytest.approx(scaled.top, rel=1e-9) == top
    assert pytest.approx(scaled.width, rel=1e-9) == width
    assert pytest.approx(scaled.height, rel=1e-9) == height
