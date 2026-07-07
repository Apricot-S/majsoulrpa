import asyncio
from random import Random

import cv2
import numpy as np
import pytest

from majsoulrpa.assets.templates.login import (
    LOGIN_1_SETTINGS_PATH,
    LOGIN_1_TEMPLATE_PATH,
)
from majsoulrpa.presentation import Region
from majsoulrpa.screens import Screen, ScreenContext, ScreenDetectionSpec
from majsoulrpa.screens.login import LoginScreen


class BrowserControllerSpy:
    def __init__(self, screenshot: bytes = b"\x89PNG\r\n\x1a\n") -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.input_texts: list[str] = []
        self.screenshot_bytes = screenshot

    async def click(self, x: float, y: float) -> None:
        self.clicked_points.append((x, y))

    async def move_mouse(self, x: float, y: float) -> None:
        _ = (x, y)

    async def input_text(self, text: str) -> None:
        self.input_texts.append(text)

    async def press_key(self, key: str) -> None:
        _ = key

    async def screenshot(self) -> bytes:
        return self.screenshot_bytes


def test_login_screen_is_screen() -> None:
    assert issubclass(LoginScreen, Screen)


def test_login_screen_detection_spec_uses_login_button_template() -> None:
    spec = LoginScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)


def test_login_button_template_assets_exist() -> None:
    assert LOGIN_1_TEMPLATE_PATH.name == "login-1.png"
    assert LOGIN_1_TEMPLATE_PATH.is_file()
    assert LOGIN_1_SETTINGS_PATH.name == "login-1.toml"
    assert LOGIN_1_SETTINGS_PATH.is_file()


def test_login_button_template_matches_synthetic_screenshot() -> None:
    encoded = np.frombuffer(LOGIN_1_TEMPLATE_PATH.read_bytes(), dtype=np.uint8)
    template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    assert template is not None
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    screenshot[435:500, 1310:1680] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success

    assert LoginScreen.detection_spec().matches(screenshot_png.tobytes())


def test_login_screen_before_callback_clicks_matched_region() -> None:
    encoded = np.frombuffer(LOGIN_1_TEMPLATE_PATH.read_bytes(), dtype=np.uint8)
    template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    assert template is not None
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    screenshot[435:500, 1310:1680] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    browser = BrowserControllerSpy(screenshot=screenshot_png.tobytes())
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    asyncio.run(screen.before_callback())

    [(x, y)] = browser.clicked_points
    assert 1310 < x < 1680
    assert 435 < y < 500
    assert browser.input_texts == []


def test_login_screen_enter_email_address_records_browser_operation() -> None:
    browser = BrowserControllerSpy()

    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    asyncio.run(screen.enter_email_address("player@example.invalid"))

    region = LoginScreen.email_address_region
    [(x, y)] = browser.clicked_points
    assert region.left < x < region.right
    assert region.top < y < region.bottom
    assert browser.input_texts == ["player@example.invalid"]
    assert isinstance(LoginScreen.email_address_region, Region)


def test_login_screen_enter_email_address_scales_region_to_viewport() -> None:
    browser = BrowserControllerSpy()
    base_region = LoginScreen.email_address_region
    LoginScreen.email_address_region = Region(
        left=300,
        top=150,
        width=6,
        height=3,
    )

    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )

    try:
        asyncio.run(screen.enter_email_address("player@example.invalid"))
    finally:
        LoginScreen.email_address_region = base_region

    [(x, y)] = browser.clicked_points
    assert 200 < x < 204
    assert 100 < y < 102
    assert browser.input_texts == ["player@example.invalid"]


def test_login_screen_rejects_non_png_screenshot() -> None:
    with pytest.raises(ValueError, match="PNG image"):
        LoginScreen.detection_spec().matches(b"not png")
