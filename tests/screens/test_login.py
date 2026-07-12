import asyncio
import logging
from importlib.resources.abc import Traversable
from random import Random
from typing import Any

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
from majsoulrpa.browser.messages import (
    YostarAuthAcceptedResponse,
    YostarAuthRejectedResponse,
)
from majsoulrpa.presentation import Region
from majsoulrpa.screens import (
    Screen,
    ScreenDetectionSpec,
)
from majsoulrpa.screens import (
    ScreenContext as FrameworkScreenContext,
)
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenInvalidArgumentError,
    ScreenInvalidOperationError,
    ScreenStaleError,
)
from majsoulrpa.screens.login import EMAIL_ADDRESS_PATTERN, LoginScreen
from tests.sniffer.fakes import EMPTY_SNIFFER_MESSAGES


def ScreenContext(  # noqa: N802
    **kwargs: Any,  # noqa: ANN401
) -> FrameworkScreenContext:
    return FrameworkScreenContext(
        sniffer_messages=EMPTY_SNIFFER_MESSAGES,
        **kwargs,
    )


class BrowserControllerSpy:
    def __init__(
        self,
        screenshot: bytes = b"\x89PNG\r\n\x1a\n",
        *screenshots: bytes,
    ) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.events: list[str] = []
        self.input_texts: list[str] = []
        self.screenshot_bytes = screenshot
        self.screenshot_queue = [screenshot, *screenshots]
        self.yostar_auth_response: (
            YostarAuthAcceptedResponse | YostarAuthRejectedResponse
        ) = YostarAuthAcceptedResponse()
        self.fail_click_number: int | None = None

    async def click(self, x: float, y: float) -> None:
        if self.fail_click_number == len(self.clicked_points) + 1:
            msg = "click failed"
            raise RuntimeError(msg)
        self.events.append("click")
        self.clicked_points.append((x, y))

    async def move_mouse(self, x: float, y: float) -> None:
        _ = (x, y)

    async def goto_url(self, url: str) -> None:
        _ = url

    async def reload(self) -> None:
        pass

    async def stop_browser_host(self) -> None:
        pass

    async def click_and_wait_for_yostar_auth(
        self,
        x: float,
        y: float,
    ) -> YostarAuthAcceptedResponse | YostarAuthRejectedResponse:
        self.events.append("click")
        self.clicked_points.append((x, y))
        return self.yostar_auth_response

    async def input_text(self, text: str) -> None:
        self.events.append("input_text")
        self.input_texts.append(text)

    async def press_key(self, key: str) -> None:
        self.events.append(f"press_key:{key}")
        _ = key

    async def screenshot(self) -> bytes:
        if self.screenshot_queue:
            return self.screenshot_queue.pop(0)
        return self.screenshot_bytes


class EmailAddressAdapterStub:
    def validate_python(self, email_address: str) -> str:
        return email_address


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
    assert LoginScreen.YOSTAR_LOGO_TEMPLATE.matches(
        _synthetic_yostar_logo_screenshot(),
    )


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


def test_login_screen_enter_email_address_records_browser_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        browser.events.append(f"sleep:{seconds}")

    monkeypatch.setattr(
        login_module,
        "EMAIL_ADDRESS_ADAPTER",
        EmailAddressAdapterStub(),
    )
    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)

    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    asyncio.run(screen.enter_email_address("player@example.invalid"))

    email_region = LoginScreen.EMAIL_ADDRESS_REGION
    send_region = LoginScreen.SEND_REGION
    [(email_x, email_y), (send_x, send_y)] = browser.clicked_points
    assert email_region.left < email_x < email_region.right
    assert email_region.top < email_y < email_region.bottom
    assert send_region.left < send_x < send_region.right
    assert send_region.top < send_y < send_region.bottom
    assert browser.input_texts == ["player@example.invalid"]
    assert sleeps == [0.5, 0.5, 0.5, 0.5, 3.0]
    assert browser.events == [
        "click",
        "sleep:0.5",
        "press_key:ControlOrMeta+A",
        "sleep:0.5",
        "press_key:Backspace",
        "sleep:0.5",
        "input_text",
        "sleep:0.5",
        "click",
        "sleep:3.0",
    ]
    assert isinstance(LoginScreen.EMAIL_ADDRESS_REGION, Region)


def test_login_screen_enter_email_address_rejects_reentry_before_60_seconds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()
    current_time = 100.0

    async def sleep(seconds: float) -> None:
        browser.events.append(f"sleep:{seconds}")

    def monotonic() -> float:
        return current_time

    monkeypatch.setattr(
        login_module,
        "EMAIL_ADDRESS_ADAPTER",
        EmailAddressAdapterStub(),
    )
    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)
    monkeypatch.setattr(login_module, "monotonic", monotonic)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    asyncio.run(screen.enter_email_address("player@example.invalid"))
    browser.clicked_points.clear()
    browser.input_texts.clear()
    browser.events.clear()

    current_time = 159.9
    with pytest.raises(
        ScreenInvalidOperationError,
        match="Email address has already been entered",
    ) as exc_info:
        asyncio.run(screen.enter_email_address("player@example.invalid"))

    assert exc_info.value.screenshot == browser.screenshot_bytes
    assert browser.clicked_points == []
    assert browser.input_texts == []
    assert browser.events == []


def test_login_screen_enter_email_address_allows_reentry_after_60_seconds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()
    current_time = 100.0

    async def sleep(seconds: float) -> None:
        browser.events.append(f"sleep:{seconds}")

    def monotonic() -> float:
        return current_time

    monkeypatch.setattr(
        login_module,
        "EMAIL_ADDRESS_ADAPTER",
        EmailAddressAdapterStub(),
    )
    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)
    monkeypatch.setattr(login_module, "monotonic", monotonic)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    asyncio.run(screen.enter_email_address("player@example.invalid"))
    browser.clicked_points.clear()
    browser.input_texts.clear()
    browser.events.clear()

    current_time = 160.0
    asyncio.run(screen.enter_email_address("player@example.invalid"))

    assert len(browser.clicked_points) == 2
    assert browser.input_texts == ["player@example.invalid"]


def test_email_address_pattern_rejects_some_rfc_valid_addresses() -> None:
    assert (
        EMAIL_ADDRESS_PATTERN.fullmatch('"player name"@example.invalid')
        is None
    )


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


def test_login_screen_high_level_api_logs_only_outer_call(
    caplog: pytest.LogCaptureFixture,
) -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    with (
        caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"),
        pytest.raises(ScreenInvalidArgumentError),
    ):
        asyncio.run(screen.enter_email_address("secret@example.invalid"))

    messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert messages == [
        "screen API called: screen=LoginScreen api=enter_email_address",
    ]
    assert "screenshot" not in caplog.text
    assert "secret@example.invalid" not in caplog.text


def test_login_screen_rejects_pattern_only_valid_address() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    assert (
        EMAIL_ADDRESS_PATTERN.fullmatch("player@sub_domain.example.invalid")
        is not None
    )

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="Email address is invalid",
    ) as exc_info:
        asyncio.run(
            screen.enter_email_address("player@sub_domain.example.invalid"),
        )

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert browser.input_texts == []


def test_login_screen_enter_email_address_scales_region_to_viewport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()
    base_region = LoginScreen.EMAIL_ADDRESS_REGION
    monkeypatch.setattr(
        login_module,
        "EMAIL_ADDRESS_ADAPTER",
        EmailAddressAdapterStub(),
    )
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

    [(email_x, email_y), (send_x, send_y)] = browser.clicked_points
    assert 200 < email_x < 204
    assert 100 < email_y < 102
    assert 734 < send_x < 762
    assert 338 < send_y < 354
    assert browser.input_texts == ["player@example.invalid"]


def test_login_screen_enter_verification_code_requires_email_address() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))

    with pytest.raises(
        ScreenInvalidOperationError,
        match="Email address must be entered before verification code",
    ) as exc_info:
        asyncio.run(screen.enter_verification_code("123456"))

    assert exc_info.value.screenshot == screenshot

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert browser.input_texts == []


@pytest.mark.parametrize(
    "verification_code",
    ["", "12345", "1234567", "12345a", "１２３４５６"],  # noqa: RUF001
)
def test_login_screen_enter_verification_code_rejects_invalid_code(
    verification_code: str,
) -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    screen._email_address_entered_at = 100.0

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="Verification code must be 6 ASCII digits",
    ) as exc_info:
        asyncio.run(screen.enter_verification_code(verification_code))

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert browser.input_texts == []


def test_login_screen_enter_verification_code_records_browser_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        browser.events.append(f"sleep:{seconds}")

    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    screen._email_address_entered_at = 100.0

    asyncio.run(screen.enter_verification_code("123456"))

    verification_code_region = LoginScreen.VERIFICATION_CODE_REGION
    login_2_region = LoginScreen.LOGIN_2_REGION
    checkbox_1_region = LoginScreen.AGREEMENT_CHECKBOX_1_REGION
    checkbox_2_region = LoginScreen.AGREEMENT_CHECKBOX_2_REGION
    agreement_button_region = LoginScreen.AGREEMENT_BUTTON_REGION
    [
        (verification_x, verification_y),
        (login_2_x, login_2_y),
        (checkbox_1_x, checkbox_1_y),
        (checkbox_2_x, checkbox_2_y),
        (agreement_button_x, agreement_button_y),
    ] = browser.clicked_points
    assert verification_code_region.left < verification_x
    assert verification_x < verification_code_region.right
    assert verification_code_region.top < verification_y
    assert verification_y < verification_code_region.bottom
    assert login_2_region.left < login_2_x < login_2_region.right
    assert login_2_region.top < login_2_y < login_2_region.bottom
    assert checkbox_1_region.left < checkbox_1_x < checkbox_1_region.right
    assert checkbox_1_region.top < checkbox_1_y < checkbox_1_region.bottom
    assert checkbox_2_region.left < checkbox_2_x < checkbox_2_region.right
    assert checkbox_2_region.top < checkbox_2_y < checkbox_2_region.bottom
    assert agreement_button_region.left < agreement_button_x
    assert agreement_button_x < agreement_button_region.right
    assert agreement_button_region.top < agreement_button_y
    assert agreement_button_y < agreement_button_region.bottom
    assert browser.input_texts == ["123456"]
    assert sleeps == [0.5, 0.5, 0.5, 0.5, 5.0, 0.5, 1.0, 2.0]
    assert browser.events == [
        "click",
        "sleep:0.5",
        "press_key:ControlOrMeta+A",
        "sleep:0.5",
        "press_key:Backspace",
        "sleep:0.5",
        "input_text",
        "sleep:0.5",
        "click",
        "sleep:5.0",
        "click",
        "sleep:0.5",
        "click",
        "sleep:1.0",
        "click",
        "sleep:2.0",
    ]

    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.enter_email_address("player@example.invalid"))


def test_login_screen_uses_720p_agreement_regions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()

    async def sleep(_seconds: float) -> None:
        pass

    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)
    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )
    screen._email_address_entered_at = 100.0

    asyncio.run(screen.enter_verification_code("123456"))

    agreement_regions = (
        LoginScreen.AGREEMENT_CHECKBOX_1_720P_REGION,
        LoginScreen.AGREEMENT_CHECKBOX_2_720P_REGION,
        LoginScreen.AGREEMENT_BUTTON_720P_REGION,
    )
    for (x, y), region in zip(
        browser.clicked_points[-3:],
        agreement_regions,
        strict=True,
    ):
        assert region.left < x < region.right
        assert region.top < y < region.bottom


def test_login_screen_scales_standard_agreement_regions_at_1440p(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    browser = BrowserControllerSpy()

    async def sleep(_seconds: float) -> None:
        pass

    monkeypatch.setattr(login_module.asyncio, "sleep", sleep)
    context = ScreenContext(
        browser=browser,
        viewport_width=2560,
        viewport_height=1440,
        rng=Random(0),
    )
    screen = LoginScreen(context=context)
    screen._email_address_entered_at = 100.0

    asyncio.run(screen.enter_verification_code("123456"))

    agreement_regions = (
        LoginScreen.AGREEMENT_CHECKBOX_1_REGION,
        LoginScreen.AGREEMENT_CHECKBOX_2_REGION,
        LoginScreen.AGREEMENT_BUTTON_REGION,
    )
    for (x, y), region in zip(
        browser.clicked_points[-3:],
        agreement_regions,
        strict=True,
    ):
        scaled_region = context.scale_region(region)
        assert scaled_region.left < x < scaled_region.right
        assert scaled_region.top < y < scaled_region.bottom


def test_login_screen_rejects_rejected_yostar_authentication() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    browser.yostar_auth_response = YostarAuthRejectedResponse(
        application_code=100303,
    )
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    screen._email_address_entered_at = 100.0

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="Verification code was rejected",
    ) as exc_info:
        asyncio.run(screen.enter_verification_code("123456"))

    assert exc_info.value.screenshot == screenshot

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="Verification code was rejected",
    ):
        asyncio.run(screen.enter_verification_code("123456"))


def test_login_screen_remains_active_when_transition_click_fails() -> None:
    browser = BrowserControllerSpy()
    browser.fail_click_number = 5
    screen = LoginScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    screen._email_address_entered_at = 100.0

    with pytest.raises(RuntimeError, match="click failed"):
        asyncio.run(screen.enter_verification_code("123456"))

    assert asyncio.run(screen.screenshot()) == browser.screenshot_bytes


def test_login_screen_rejects_non_png_screenshot() -> None:
    with pytest.raises(ValueError, match="PNG image"):
        LoginScreen.detection_spec().matches(b"not png")
