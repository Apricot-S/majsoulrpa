import asyncio
from importlib.resources.abc import Traversable
from random import Random

import cv2
import numpy as np
import pytest

import majsoulrpa.screens.login as login_module
from majsoulrpa.assets.templates.login import (
    LOGIN_1_SETTINGS_PATH,
    LOGIN_1_TEMPLATE_PATH,
    YOSTAR_LOGO_SETTINGS_PATH,
    YOSTAR_LOGO_TEMPLATE_PATH,
)
from majsoulrpa.presentation import Region
from majsoulrpa.screens import Screen, ScreenContext, ScreenDetectionSpec
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenInvalidArgumentError,
)
from majsoulrpa.screens.login import YOSTAR_LOGO_TEMPLATE, LoginScreen


class BrowserControllerSpy:
    def __init__(
        self,
        screenshot: bytes = b"\x89PNG\r\n\x1a\n",
        *screenshots: bytes,
    ) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.input_texts: list[str] = []
        self.screenshot_bytes = screenshot
        self.screenshot_queue = [screenshot, *screenshots]

    async def click(self, x: float, y: float) -> None:
        self.clicked_points.append((x, y))

    async def move_mouse(self, x: float, y: float) -> None:
        _ = (x, y)

    async def goto_url(self, url: str) -> None:
        _ = url

    async def reload(self) -> None:
        pass

    async def stop_browser_host(self) -> None:
        pass

    async def input_text(self, text: str) -> None:
        self.input_texts.append(text)

    async def press_key(self, key: str) -> None:
        _ = key

    async def screenshot(self) -> bytes:
        if self.screenshot_queue:
            return self.screenshot_queue.pop(0)
        return self.screenshot_bytes


def _synthetic_template_screenshot(
    *,
    template_path: Traversable,
    left: int,
    top: int,
    width: int,
    height: int,
) -> bytes:
    encoded = np.frombuffer(template_path.read_bytes(), dtype=np.uint8)
    template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    assert template is not None
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    screenshot[top : top + height, left : left + width] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def _synthetic_blank_screenshot() -> bytes:
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def _synthetic_login_button_screenshot() -> bytes:
    return _synthetic_template_screenshot(
        template_path=LOGIN_1_TEMPLATE_PATH,
        left=1310,
        top=435,
        width=370,
        height=65,
    )


def _synthetic_yostar_logo_screenshot() -> bytes:
    return _synthetic_template_screenshot(
        template_path=YOSTAR_LOGO_TEMPLATE_PATH,
        left=865,
        top=347,
        width=190,
        height=50,
    )


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


def test_yostar_logo_template_assets_exist() -> None:
    assert YOSTAR_LOGO_TEMPLATE_PATH.name == "yostar-logo.png"
    assert YOSTAR_LOGO_TEMPLATE_PATH.is_file()
    assert YOSTAR_LOGO_SETTINGS_PATH.name == "yostar-logo.toml"
    assert YOSTAR_LOGO_SETTINGS_PATH.is_file()


def test_yostar_logo_template_matches_synthetic_screenshot() -> None:
    assert YOSTAR_LOGO_TEMPLATE.matches(_synthetic_yostar_logo_screenshot())


def test_login_button_template_matches_synthetic_screenshot() -> None:
    assert LoginScreen.detection_spec().matches(
        _synthetic_login_button_screenshot(),
    )


def test_login_screen_before_callback_clicks_matched_region(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = BrowserControllerSpy(
        _synthetic_login_button_screenshot(),
        _synthetic_yostar_logo_screenshot(),
    )
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    [(x, y)] = browser.clicked_points
    assert 1310 < x < 1680
    assert 435 < y < 500
    assert sleeps == [1.0, 0.5]
    assert browser.input_texts == []


def test_login_screen_before_callback_raises_without_login_button() -> None:
    browser = BrowserControllerSpy(_synthetic_blank_screenshot())
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    with pytest.raises(ScreenDetectionError, match="login button") as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == browser.screenshot_bytes
    assert browser.clicked_points == []


def test_login_screen_before_callback_raises_when_yostar_logo_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    yostar_missing_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_login_button_screenshot(),
        yostar_missing_screenshot,
    )
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)

    with pytest.raises(ScreenDetectionError, match="Yostar logo") as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == yostar_missing_screenshot
    assert browser.clicked_points


def test_login_screen_enter_email_address_records_browser_operation() -> None:
    browser = BrowserControllerSpy()

    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    asyncio.run(screen.enter_email_address("player@example.invalid"))

    region = LoginScreen.EMAIL_ADDRESS_REGION
    [(x, y)] = browser.clicked_points
    assert region.left < x < region.right
    assert region.top < y < region.bottom
    assert browser.input_texts == ["player@example.invalid"]
    assert isinstance(LoginScreen.EMAIL_ADDRESS_REGION, Region)


def test_login_screen_enter_email_address_rejects_invalid_address() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="is not available for Yostar login",
    ) as exc_info:
        asyncio.run(screen.enter_email_address("not an email address"))

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert browser.input_texts == []


def test_login_screen_enter_email_address_scales_region_to_viewport() -> None:
    browser = BrowserControllerSpy()
    base_region = LoginScreen.EMAIL_ADDRESS_REGION
    LoginScreen.EMAIL_ADDRESS_REGION = Region(
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
        LoginScreen.EMAIL_ADDRESS_REGION = base_region

    [(x, y)] = browser.clicked_points
    assert 200 < x < 204
    assert 100 < y < 102
    assert browser.input_texts == ["player@example.invalid"]


def test_login_screen_rejects_non_png_screenshot() -> None:
    with pytest.raises(ValueError, match="PNG image"):
        LoginScreen.detection_spec().matches(b"not png")
