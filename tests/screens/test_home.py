from importlib.resources.abc import Traversable

import cv2
import numpy as np

from majsoulrpa.assets.templates.home import (
    SUMMON_SETTINGS_PATH,
    SUMMON_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.screens.home import HomeScreen


def _synthetic_template_screenshot(
    *,
    template_path: Traversable,
    settings_path: Traversable,
) -> bytes:
    encoded = np.frombuffer(template_path.read_bytes(), dtype=np.uint8)
    template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    assert template is not None
    settings = TemplateMatchSettings.from_toml_file(settings_path)
    region = settings.region
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    left = round(region.left)
    top = round(region.top)
    width = round(region.width)
    height = round(region.height)
    screenshot[top : top + height, left : left + width] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def _synthetic_blank_screenshot() -> bytes:
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def test_home_screen_is_screen() -> None:
    assert issubclass(HomeScreen, Screen)


def test_summon_template_assets_exist() -> None:
    assert SUMMON_TEMPLATE_PATH.name == "summon.png"
    assert SUMMON_TEMPLATE_PATH.is_file()
    assert SUMMON_SETTINGS_PATH.name == "summon.toml"
    assert SUMMON_SETTINGS_PATH.is_file()


def test_home_screen_detection_spec_uses_summon_template() -> None:
    spec = HomeScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    assert spec.matches(
        _synthetic_template_screenshot(
            template_path=SUMMON_TEMPLATE_PATH,
            settings_path=SUMMON_SETTINGS_PATH,
        ),
    )


def test_home_screen_does_not_match_blank_screenshot() -> None:
    assert not HomeScreen.detection_spec().matches(
        _synthetic_blank_screenshot(),
    )
