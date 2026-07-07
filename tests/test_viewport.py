import pytest

from majsoulrpa.viewport import viewport_width_for_height


@pytest.mark.parametrize(
    ("height", "expected_width"),
    [
        (720, 1280),
        (1080, 1920),
        (1440, 2560),
    ],
)
def test_viewport_width_for_height_uses_base_aspect_ratio(
    height: int,
    expected_width: int,
) -> None:
    assert viewport_width_for_height(height) == expected_width
