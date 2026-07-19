from importlib.resources.abc import Traversable

import pytest

from majsoulrpa.assets.templates.match import (
    SEAT_INDICATOR_SETTINGS_PATH,
    SEAT_INDICATOR_TEMPLATE_PATHS,
)
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.screens.match import MatchScreen
from tests.screens.home._support import (
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)


def test_seat_indicator_template_assets_exist() -> None:
    assert SEAT_INDICATOR_SETTINGS_PATH.name == "seat-indicator.toml"
    assert SEAT_INDICATOR_SETTINGS_PATH.is_file()
    assert tuple(path.name for path in SEAT_INDICATOR_TEMPLATE_PATHS) == (
        "seat-indicator-0.png",
        "seat-indicator-1.png",
        "seat-indicator-2.png",
        "seat-indicator-3.png",
    )
    assert all(path.is_file() for path in SEAT_INDICATOR_TEMPLATE_PATHS)


def test_match_screen_is_screen() -> None:
    assert issubclass(MatchScreen, Screen)


@pytest.mark.parametrize("template_path", SEAT_INDICATOR_TEMPLATE_PATHS)
def test_match_screen_detection_spec_matches_each_seat_indicator(
    template_path: Traversable,
) -> None:
    spec = MatchScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    assert spec.matches(
        _synthetic_template_screenshot(
            template_path=template_path,
            settings_path=SEAT_INDICATOR_SETTINGS_PATH,
        ),
    )


def test_match_screen_does_not_match_blank_screenshot() -> None:
    assert not MatchScreen.detection_spec().matches(
        _synthetic_blank_screenshot(),
    )
