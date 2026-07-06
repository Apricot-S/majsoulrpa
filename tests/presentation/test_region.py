from random import Random

import pytest

from majsoulrpa.presentation import Region


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


def test_region_random_point_rejects_non_positive_boundary_sigma() -> None:
    region = Region(left=10, top=20, width=30, height=40)

    with pytest.raises(ValueError, match="boundary_sigma"):
        region.random_point(boundary_sigma=0, rng=Random(0))


def test_region_random_point_rejects_non_positive_size() -> None:
    region = Region(left=10, top=20, width=0, height=40)

    with pytest.raises(ValueError, match="region size"):
        region.random_point(rng=Random(0))
