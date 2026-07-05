import asyncio

import pytest

from majsoulrpa.presentation import Region
from majsoulrpa.screens import (
    LoginScreen,
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
)


class BrowserControllerSpy:
    def __init__(self) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.input_texts: list[str] = []

    async def click(self, x: float, y: float) -> None:
        self.clicked_points.append((x, y))

    async def input_text(self, text: str) -> None:
        self.input_texts.append(text)


def test_login_screen_is_screen() -> None:
    assert issubclass(LoginScreen, Screen)


def test_login_screen_detection_spec_uses_template_predicate() -> None:
    spec = LoginScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    with pytest.raises(RuntimeError, match="template matcher"):
        spec.matches(object())


def test_login_screen_enter_email_address_records_browser_operation() -> None:
    browser = BrowserControllerSpy()

    screen = LoginScreen(
        context=ScreenContext(browser=browser),
    )

    asyncio.run(screen.enter_email_address("player@example.invalid"))

    region = LoginScreen.email_address_region
    assert browser.clicked_points == [
        (region.left + region.width / 2, region.top + region.height / 2),
    ]
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
        ),
    )

    try:
        asyncio.run(screen.enter_email_address("player@example.invalid"))
    finally:
        LoginScreen.email_address_region = base_region

    assert browser.clicked_points == [(202, 101)]
    assert browser.input_texts == ["player@example.invalid"]
