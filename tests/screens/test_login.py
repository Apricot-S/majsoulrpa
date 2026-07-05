import asyncio

import pytest

from majsoulrpa.presentation import Region
from majsoulrpa.screens import (
    BrowserOperation,
    LoginScreen,
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
)


def test_login_screen_is_screen() -> None:
    assert issubclass(LoginScreen, Screen)


def test_login_screen_detection_spec_uses_template_predicate() -> None:
    spec = LoginScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    with pytest.raises(RuntimeError, match="template matcher"):
        spec.matches(object())


def test_login_screen_enter_email_address_records_browser_operation() -> None:
    operations: list[BrowserOperation] = []

    async def record(operation: BrowserOperation) -> None:
        operations.append(operation)

    screen = LoginScreen(
        context=ScreenContext(record_browser_operation=record),
    )

    asyncio.run(screen.enter_email_address("player@example.invalid"))

    assert operations == [
        BrowserOperation(
            name="fill_region",
            parameters={
                "region": LoginScreen.email_address_region,
                "value": "player@example.invalid",
            },
        ),
    ]
    assert isinstance(LoginScreen.email_address_region, Region)


def test_login_screen_enter_email_address_scales_region_to_viewport() -> None:
    operations: list[BrowserOperation] = []
    base_region = LoginScreen.email_address_region
    LoginScreen.email_address_region = Region(
        left=300,
        top=150,
        width=6,
        height=3,
    )

    async def record(operation: BrowserOperation) -> None:
        operations.append(operation)

    screen = LoginScreen(
        context=ScreenContext(
            record_browser_operation=record,
            viewport_width=1280,
            viewport_height=720,
        ),
    )

    try:
        asyncio.run(screen.enter_email_address("player@example.invalid"))
    finally:
        LoginScreen.email_address_region = base_region

    assert operations == [
        BrowserOperation(
            name="fill_region",
            parameters={
                "region": Region(left=200, top=100, width=4, height=2),
                "value": "player@example.invalid",
            },
        ),
    ]
