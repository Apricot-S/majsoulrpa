from majsoulrpa.presentation import Region


def test_region_scales_to_viewport_size() -> None:
    region = Region(left=300, top=150, width=6, height=3)

    assert region.scale_to_viewport(width=1280, height=720) == Region(
        left=200,
        top=100,
        width=4,
        height=2,
    )
