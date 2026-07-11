import asyncio
from importlib.resources.abc import Traversable
from random import Random

import cv2
import numpy as np
import pytest

import majsoulrpa.screens.home as home_module
from majsoulrpa.assets.templates.home import (
    EVENT_CLOSE_SETTINGS_PATH,
    EVENT_CLOSE_TEMPLATE_PATH,
    MAIL_CLOSE_SETTINGS_PATH,
    MAIL_CLOSE_TEMPLATE_PATH,
    NOTIFICATION_CLOSE_SETTINGS_PATH,
    NOTIFICATION_CLOSE_TEMPLATE_PATH,
    REWARDS_CONFIRM_SETTINGS_PATH,
    REWARDS_CONFIRM_TEMPLATE_PATH,
    REWARDS_SIGN_IN_SETTINGS_PATH,
    REWARDS_SIGN_IN_TEMPLATE_PATH,
    SUMMON_SETTINGS_PATH,
    SUMMON_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens import Screen, ScreenContext, ScreenDetectionSpec
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenUnexpectedStateError,
)
from majsoulrpa.screens.home import HomeScreen


class BrowserControllerSpy:
    def __init__(self, screenshot: bytes, *screenshots: bytes) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.screenshot_bytes = screenshot
        self.screenshot_queue = [screenshot, *screenshots]
        self.screenshot_count = 0

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

    async def click_and_wait_for_yostar_auth(
        self,
        x: float,
        y: float,
    ) -> object:
        _ = (x, y)
        return object()

    async def input_text(self, text: str) -> None:
        _ = text

    async def press_key(self, key: str) -> None:
        _ = key

    async def screenshot(self) -> bytes:
        self.screenshot_count += 1
        if self.screenshot_queue:
            return self.screenshot_queue.pop(0)
        return self.screenshot_bytes


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


def test_notification_close_template_assets_exist() -> None:
    assert NOTIFICATION_CLOSE_TEMPLATE_PATH.name == "notification-close.png"
    assert NOTIFICATION_CLOSE_TEMPLATE_PATH.is_file()
    assert NOTIFICATION_CLOSE_SETTINGS_PATH.name == "notification-close.toml"
    assert NOTIFICATION_CLOSE_SETTINGS_PATH.is_file()


def test_event_close_template_assets_exist() -> None:
    assert EVENT_CLOSE_TEMPLATE_PATH.name == "event-close.png"
    assert EVENT_CLOSE_TEMPLATE_PATH.is_file()
    assert EVENT_CLOSE_SETTINGS_PATH.name == "event-close.toml"
    assert EVENT_CLOSE_SETTINGS_PATH.is_file()


def test_mail_close_template_assets_exist() -> None:
    assert MAIL_CLOSE_TEMPLATE_PATH.name == "mail-close.png"
    assert MAIL_CLOSE_TEMPLATE_PATH.is_file()
    assert MAIL_CLOSE_SETTINGS_PATH.name == "mail-close.toml"
    assert MAIL_CLOSE_SETTINGS_PATH.is_file()


def test_rewards_template_assets_exist() -> None:
    assert REWARDS_SIGN_IN_TEMPLATE_PATH.name == "rewards-sign-in.png"
    assert REWARDS_SIGN_IN_TEMPLATE_PATH.is_file()
    assert REWARDS_SIGN_IN_SETTINGS_PATH.name == "rewards-sign-in.toml"
    assert REWARDS_SIGN_IN_SETTINGS_PATH.is_file()
    assert REWARDS_CONFIRM_TEMPLATE_PATH.name == "rewards-confirm.png"
    assert REWARDS_CONFIRM_TEMPLATE_PATH.is_file()
    assert REWARDS_CONFIRM_SETTINGS_PATH.name == "rewards-confirm.toml"
    assert REWARDS_CONFIRM_SETTINGS_PATH.is_file()


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


def test_home_screen_before_callback_closes_notification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=NOTIFICATION_CLOSE_TEMPLATE_PATH,
            settings_path=NOTIFICATION_CLOSE_SETTINGS_PATH,
        ),
        _synthetic_blank_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    [(x, y)] = browser.clicked_points
    assert 1612 < x < 1644
    assert 174 < y < 206
    assert sleeps == [1.0]


def test_home_screen_before_callback_does_nothing_without_notification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = BrowserControllerSpy(_synthetic_blank_screenshot())
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert browser.clicked_points == []
    assert sleeps == []


@pytest.mark.parametrize(
    (
        "first_template_path",
        "first_settings_path",
        "second_template_path",
        "second_settings_path",
    ),
    [
        (
            NOTIFICATION_CLOSE_TEMPLATE_PATH,
            NOTIFICATION_CLOSE_SETTINGS_PATH,
            EVENT_CLOSE_TEMPLATE_PATH,
            EVENT_CLOSE_SETTINGS_PATH,
        ),
        (
            EVENT_CLOSE_TEMPLATE_PATH,
            EVENT_CLOSE_SETTINGS_PATH,
            NOTIFICATION_CLOSE_TEMPLATE_PATH,
            NOTIFICATION_CLOSE_SETTINGS_PATH,
        ),
    ],
)
def test_home_screen_closes_notification_and_event_in_either_order(
    monkeypatch: pytest.MonkeyPatch,
    first_template_path: Traversable,
    first_settings_path: Traversable,
    second_template_path: Traversable,
    second_settings_path: Traversable,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=first_template_path,
            settings_path=first_settings_path,
        ),
        _synthetic_template_screenshot(
            template_path=second_template_path,
            settings_path=second_settings_path,
        ),
        _synthetic_blank_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 2
    assert sleeps == [1.0, 1.0]
    assert browser.screenshot_count == 3


@pytest.mark.parametrize(
    ("ordered_assets"),
    [
        (
            (MAIL_CLOSE_TEMPLATE_PATH, MAIL_CLOSE_SETTINGS_PATH),
            (
                NOTIFICATION_CLOSE_TEMPLATE_PATH,
                NOTIFICATION_CLOSE_SETTINGS_PATH,
            ),
            (EVENT_CLOSE_TEMPLATE_PATH, EVENT_CLOSE_SETTINGS_PATH),
        ),
        (
            (EVENT_CLOSE_TEMPLATE_PATH, EVENT_CLOSE_SETTINGS_PATH),
            (
                NOTIFICATION_CLOSE_TEMPLATE_PATH,
                NOTIFICATION_CLOSE_SETTINGS_PATH,
            ),
            (MAIL_CLOSE_TEMPLATE_PATH, MAIL_CLOSE_SETTINGS_PATH),
        ),
    ],
)
def test_home_screen_closes_mail_with_other_screens_in_either_order(
    monkeypatch: pytest.MonkeyPatch,
    ordered_assets: tuple[tuple[Traversable, Traversable], ...],
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    screenshots = [
        _synthetic_template_screenshot(
            template_path=template_path,
            settings_path=settings_path,
        )
        for template_path, settings_path in ordered_assets
    ]
    browser = BrowserControllerSpy(
        screenshots[0],
        *screenshots[1:],
        _synthetic_blank_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 3
    assert sleeps == [1.0, 1.0, 1.0]
    assert browser.screenshot_count == 4


def test_home_screen_raises_when_same_close_template_is_detected_twice(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    notification_screenshot = _synthetic_template_screenshot(
        template_path=NOTIFICATION_CLOSE_TEMPLATE_PATH,
        settings_path=NOTIFICATION_CLOSE_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(
        notification_screenshot,
        notification_screenshot,
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenUnexpectedStateError,
        match=r"notification-close.*more than once",
    ) as exc_info:
        asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 1
    assert sleeps == [1.0]
    assert browser.screenshot_count == 2
    assert exc_info.value.screenshot == notification_screenshot


def test_home_screen_raises_when_mail_close_is_detected_twice(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    mail_screenshot = _synthetic_template_screenshot(
        template_path=MAIL_CLOSE_TEMPLATE_PATH,
        settings_path=MAIL_CLOSE_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(mail_screenshot, mail_screenshot)
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenUnexpectedStateError,
        match=r"mail-close.*more than once",
    ) as exc_info:
        asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 1
    assert sleeps == [1.0]
    assert browser.screenshot_count == 2
    assert exc_info.value.screenshot == mail_screenshot


@pytest.mark.parametrize(
    ("rewards_first", "expected_sleeps"),
    [
        (True, [2.0, 0.5, 1.0]),
        (False, [1.0, 2.0, 0.5]),
    ],
)
def test_home_screen_processes_rewards_and_close_in_either_order(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rewards_first: bool,
    expected_sleeps: list[float],
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    rewards_sign_in = _synthetic_template_screenshot(
        template_path=REWARDS_SIGN_IN_TEMPLATE_PATH,
        settings_path=REWARDS_SIGN_IN_SETTINGS_PATH,
    )
    rewards_confirm = _synthetic_template_screenshot(
        template_path=REWARDS_CONFIRM_TEMPLATE_PATH,
        settings_path=REWARDS_CONFIRM_SETTINGS_PATH,
    )
    notification = _synthetic_template_screenshot(
        template_path=NOTIFICATION_CLOSE_TEMPLATE_PATH,
        settings_path=NOTIFICATION_CLOSE_SETTINGS_PATH,
    )
    screenshots = (
        [rewards_sign_in, rewards_confirm, notification]
        if rewards_first
        else [notification, rewards_sign_in, rewards_confirm]
    )
    browser = BrowserControllerSpy(
        screenshots[0],
        *screenshots[1:],
        _synthetic_blank_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 3
    assert sleeps == expected_sleeps
    assert browser.screenshot_count == 4


def test_home_screen_raises_when_rewards_confirm_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_confirm_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=REWARDS_SIGN_IN_TEMPLATE_PATH,
            settings_path=REWARDS_SIGN_IN_SETTINGS_PATH,
        ),
        missing_confirm_screenshot,
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="rewards-confirm was not found",
    ) as exc_info:
        asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 1
    assert sleeps == [2.0]
    assert browser.screenshot_count == 2
    assert exc_info.value.screenshot == missing_confirm_screenshot
