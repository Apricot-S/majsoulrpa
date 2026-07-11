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
    NOTIFICATION_CLOSE_SETTINGS_PATH,
    NOTIFICATION_CLOSE_TEMPLATE_PATH,
    SUMMON_SETTINGS_PATH,
    SUMMON_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens import Screen, ScreenContext, ScreenDetectionSpec
from majsoulrpa.screens.errors import ScreenUnexpectedStateError
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
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 2
    assert sleeps == [1.0, 1.0]
    assert browser.screenshot_count == 2


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
