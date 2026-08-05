import math
from random import Random

import pytest

from majsoulrpa.presentation import Region


class FailOnUseRandom(Random):
    def normalvariate(
        self,
        mu: float = 0.0,
        sigma: float = 1.0,
    ) -> float:
        _ = mu, sigma
        msg = "random source must not be used"
        raise AssertionError(msg)


class FalseyCenterRandom(Random):
    def __bool__(self) -> bool:
        return False

    def normalvariate(
        self,
        mu: float = 0.0,
        sigma: float = 1.0,
    ) -> float:
        _ = sigma
        return mu


def test_region_scales_to_viewport_size() -> None:
    region = Region(left=300, top=150, width=6, height=3)

    assert region.scale_to_viewport(width=1280, height=720) == Region(
        left=200,
        top=100,
        width=4,
        height=2,
    )


def test_region_rejects_too_small_scaled_size() -> None:
    region = Region(left=0, top=0, width=0.1, height=1)

    with pytest.raises(ValueError, match="scaled region size"):
        region.scale_to_viewport(width=1280, height=720)


def test_region_random_point_is_inside_region() -> None:
    region = Region(left=10, top=20, width=30, height=40)

    x, y = region.random_point(rng=Random(0))

    assert region.left < x < region.right
    assert region.top < y < region.bottom


def test_region_random_point_uses_falsey_random_source() -> None:
    region = Region(left=10, top=20, width=30, height=40)

    point = region.random_point(rng=FalseyCenterRandom())

    assert point == (25.0, 40.0)


def test_region_random_point_rejects_non_positive_boundary_sigma() -> None:
    region = Region(left=10, top=20, width=30, height=40)

    with pytest.raises(ValueError, match="boundary_sigma"):
        region.random_point(boundary_sigma=0, rng=Random(0))


def test_region_rejects_non_positive_size() -> None:
    with pytest.raises(ValueError, match="region size"):
        Region(left=10, top=20, width=0, height=40)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("field", ["left", "top", "width", "height"])
def test_region_rejects_non_finite_field(field: str, value: float) -> None:
    values = {"left": 10.0, "top": 20.0, "width": 30.0, "height": 40.0}
    values[field] = value

    with pytest.raises(ValueError, match="finite"):
        Region(**values)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("field", ["width", "height"])
def test_region_scale_rejects_non_finite_viewport_size(
    field: str,
    value: float,
) -> None:
    region = Region(left=10, top=20, width=30, height=40)
    viewport = {"width": 1920, "height": 1080}
    viewport[field] = value

    with pytest.raises(ValueError, match="viewport size must be finite"):
        region.scale_to_viewport(**viewport)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_region_random_point_rejects_non_finite_boundary_sigma(
    value: float,
) -> None:
    region = Region(left=10, top=20, width=30, height=40)

    with pytest.raises(ValueError, match="boundary_sigma must be finite"):
        region.random_point(
            boundary_sigma=value,
            rng=FailOnUseRandom(),
        )
