import asyncio
import datetime
import logging
from importlib.resources.abc import Traversable
from inspect import signature
from random import Random
from typing import Any

import cv2
import numpy as np
import pytest

import majsoulrpa.screens.home as home_module
from majsoulrpa.assets.templates.home import (
    EVENT_CLOSE_SETTINGS_PATH,
    EVENT_CLOSE_TEMPLATE_PATH,
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
    JADE_SETTINGS_PATH,
    JADE_TEMPLATE_PATH,
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
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens import (
    Screen,
    ScreenDetectionSpec,
)
from majsoulrpa.screens import (
    ScreenContext as FrameworkScreenContext,
)
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenStaleError,
    ScreenUnexpectedStateError,
)
from majsoulrpa.screens.home import HomeScreen, Length, Mode, ThinkingTime
from majsoulrpa.sniffer.events import DecodedNotice, Direction, RawNotice
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.sniffer.fakes import EMPTY_SNIFFER_MESSAGES


def ScreenContext(  # noqa: N802
    **kwargs: Any,  # noqa: ANN401
) -> FrameworkScreenContext:
    kwargs.setdefault("sniffer_messages", EMPTY_SNIFFER_MESSAGES)
    return FrameworkScreenContext(
        **kwargs,
    )


class BrowserControllerSpy:
    def __init__(self, screenshot: bytes, *screenshots: bytes) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.screenshot_bytes = screenshot
        self.screenshot_queue = [screenshot, *screenshots]
        self.screenshot_count = 0
        self.events: list[str] = []

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
        self.events.append("screenshot")
        self.screenshot_count += 1
        if self.screenshot_queue:
            return self.screenshot_queue.pop(0)
        return self.screenshot_bytes


def _synthetic_template_screenshot(
    *,
    template_path: Traversable,
    settings_path: Traversable,
) -> bytes:
    return _synthetic_templates_screenshot(
        ((template_path, settings_path),),
    )


def _synthetic_templates_screenshot(
    assets: tuple[tuple[Traversable, Traversable], ...],
) -> bytes:
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    for template_path, settings_path in assets:
        encoded = np.frombuffer(template_path.read_bytes(), dtype=np.uint8)
        template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
        assert template is not None
        settings = TemplateMatchSettings.from_toml_file(settings_path)
        region = settings.region
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


def _synthetic_home_ready_screenshot() -> bytes:
    return _synthetic_templates_screenshot(
        (
            (
                TOURNAMENT_MATCH_TEMPLATE_PATH,
                TOURNAMENT_MATCH_SETTINGS_PATH,
            ),
            (FRIENDLY_MATCH_TEMPLATE_PATH, FRIENDLY_MATCH_SETTINGS_PATH),
        ),
    )


def _message_queue(*names: str) -> SnifferMessageQueue:
    queue = SnifferMessageQueue(capacity=10, max_payload_bytes=1024)
    for name in names:
        queue.enqueue(
            DecodedNotice(
                raw=RawNotice(
                    direction=Direction.INBOUND,
                    name=name,
                    payload=b"synthetic",
                    observed_at=datetime.datetime(
                        2026,
                        1,
                        2,
                        tzinfo=datetime.UTC,
                    ),
                ),
                message={},
            ),
        )
    return queue


def test_home_screen_is_screen() -> None:
    assert issubclass(HomeScreen, Screen)


def test_room_creation_enums_have_expected_members() -> None:
    assert list(Mode) == [Mode.FOUR_PLAYER, Mode.THREE_PLAYER]
    assert list(Length) == [
        Length.ONE_GAME,
        Length.EAST_ONLY,
        Length.TWO_WIND_MATCH,
        Length.VS_AI,
    ]
    assert list(ThinkingTime) == [
        ThinkingTime.THREE_PLUS_FIVE,
        ThinkingTime.FIVE_PLUS_TEN,
        ThinkingTime.FIVE_PLUS_TWENTY,
        ThinkingTime.SIXTY_PLUS_ZERO,
        ThinkingTime.THREE_HUNDRED_PLUS_ZERO,
    ]


def test_create_room_defaults_to_four_player_two_wind_five_plus_twenty(
    caplog: pytest.LogCaptureFixture,
) -> None:
    screen = HomeScreen()
    parameters = signature(HomeScreen.create_room).parameters

    assert parameters["mode"].default is Mode.FOUR_PLAYER
    assert parameters["length"].default is Length.TWO_WIND_MATCH
    assert parameters["thinking_time"].default is ThinkingTime.FIVE_PLUS_TWENTY

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        result = asyncio.run(screen.create_room())

    assert result is None
    assert (
        "screen API called: screen=HomeScreen api=create_room" in caplog.text
    )


def test_create_room_accepts_each_enum_value() -> None:
    screen = HomeScreen()

    async def create_rooms() -> list[None]:
        results = [await screen.create_room(mode=mode) for mode in Mode]
        results.extend(
            [await screen.create_room(length=length) for length in Length],
        )
        results.extend(
            [
                await screen.create_room(thinking_time=thinking_time)
                for thinking_time in ThinkingTime
            ],
        )
        return results

    assert asyncio.run(create_rooms()) == [None] * (
        len(Mode) + len(Length) + len(ThinkingTime)
    )


def test_create_room_rejects_stale_home_screen() -> None:
    screenshot = _synthetic_blank_screenshot()
    screen = HomeScreen(
        context=ScreenContext(browser=BrowserControllerSpy(screenshot)),
    )
    screen._mark_stale()

    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(screen.create_room())

    assert exc_info.value.screenshot == screenshot


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


def test_jade_template_assets_exist() -> None:
    assert JADE_TEMPLATE_PATH.name == "jade.png"
    assert JADE_TEMPLATE_PATH.is_file()
    assert JADE_SETTINGS_PATH.name == "jade.toml"
    assert JADE_SETTINGS_PATH.is_file()


def test_home_before_callback_skips_jade_without_month_ticket_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = BrowserControllerSpy(_synthetic_home_ready_screenshot())
    queue = _message_queue(".lq.Unrelated")
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=queue,
            rng=Random(0),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert browser.clicked_points == []
    assert sleeps == [1.0]
    assert queue.get_nowait() is None


def test_discard_sniffer_messages_logs_each_message_at_info(
    caplog: pytest.LogCaptureFixture,
) -> None:
    queue = _message_queue(".lq.Test.first", ".lq.Test.second")
    screen = HomeScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(_synthetic_blank_screenshot()),
            sniffer_messages=queue,
        ),
    )

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.home"):
        screen._discard_sniffer_messages()

    records = [
        record
        for record in caplog.records
        if record.name == "majsoulrpa.screens.home"
    ]
    assert [record.levelno for record in records] == [
        logging.INFO,
        logging.INFO,
    ]
    assert [record.getMessage() for record in records] == [
        (
            'Sniffer message: {"raw":{"direction":"inbound",'
            '"name":".lq.Test.first",'
            '"observed_at":"2026-01-02T00:00:00+00:00"},"message":{}}'
        ),
        (
            'Sniffer message: {"raw":{"direction":"inbound",'
            '"name":".lq.Test.second",'
            '"observed_at":"2026-01-02T00:00:00+00:00"},"message":{}}'
        ),
    ]
    assert "synthetic" not in caplog.text
    assert queue.get_nowait() is None


def test_home_before_callback_retries_and_clicks_jade_for_month_ticket(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    blank = _synthetic_blank_screenshot()
    jade = _synthetic_template_screenshot(
        template_path=JADE_TEMPLATE_PATH,
        settings_path=JADE_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(
        blank,
        jade,
        _synthetic_home_ready_screenshot(),
    )
    queue = _message_queue(
        ".lq.Unrelated",
        ".lq.Lobby.payMonthTicket",
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=queue,
            rng=Random(0),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 1
    assert sleeps == [0.5, 0.5, 1.0]
    assert queue.get_nowait() is None


def test_month_ticket_check_puts_back_all_messages() -> None:
    jade = _synthetic_template_screenshot(
        template_path=JADE_TEMPLATE_PATH,
        settings_path=JADE_SETTINGS_PATH,
    )
    queue = _message_queue(
        ".lq.Unrelated",
        ".lq.Lobby.payMonthTicket",
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(jade),
            sniffer_messages=queue,
            rng=Random(0),
        ),
    )

    asyncio.run(screen._process_month_ticket())

    first = queue.get_nowait()
    second = queue.get_nowait()
    assert first is not None
    assert second is not None
    assert first.raw.name == ".lq.Unrelated"
    assert second.raw.name == ".lq.Lobby.payMonthTicket"


def test_home_before_callback_raises_if_jade_is_not_found_in_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blank = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(blank)
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                ".lq.Lobby.payMonthTicket",
            ),
            rng=Random(0),
        ),
    )
    monkeypatch.setattr(home_module, "JADE_WAIT_TIMEOUT_SECONDS", 0.001)

    with pytest.raises(
        ScreenDetectionError,
        match="jade was not found within 5 seconds",
    ) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == blank


def test_match_button_template_assets_exist() -> None:
    assert TOURNAMENT_MATCH_TEMPLATE_PATH.name == "tournament-match.png"
    assert TOURNAMENT_MATCH_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_MATCH_SETTINGS_PATH.name == "tournament-match.toml"
    assert TOURNAMENT_MATCH_SETTINGS_PATH.is_file()
    assert FRIENDLY_MATCH_TEMPLATE_PATH.name == "friendly-match.png"
    assert FRIENDLY_MATCH_TEMPLATE_PATH.is_file()
    assert FRIENDLY_MATCH_SETTINGS_PATH.name == "friendly-match.toml"
    assert FRIENDLY_MATCH_SETTINGS_PATH.is_file()


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
        _synthetic_home_ready_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    [(x, y)] = browser.clicked_points
    assert 1612 < x < 1644
    assert 174 < y < 206
    assert sleeps == [1.0, 1.0]


def test_home_screen_before_callback_does_nothing_without_notification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        browser.events.append(f"sleep:{seconds}")

    browser = BrowserControllerSpy(_synthetic_home_ready_screenshot())
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert browser.clicked_points == []
    assert sleeps == [1.0]
    assert browser.events == ["sleep:1.0", "screenshot"]


@pytest.mark.parametrize(
    ("present_template_path", "present_settings_path", "missing_name"),
    [
        (
            FRIENDLY_MATCH_TEMPLATE_PATH,
            FRIENDLY_MATCH_SETTINGS_PATH,
            "tournament-match",
        ),
        (
            TOURNAMENT_MATCH_TEMPLATE_PATH,
            TOURNAMENT_MATCH_SETTINGS_PATH,
            "friendly-match",
        ),
    ],
)
def test_home_screen_raises_when_match_button_is_missing(
    present_template_path: Traversable,
    present_settings_path: Traversable,
    missing_name: str,
) -> None:
    screenshot = _synthetic_template_screenshot(
        template_path=present_template_path,
        settings_path=present_settings_path,
    )
    browser = BrowserControllerSpy(screenshot)
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    with pytest.raises(
        ScreenDetectionError,
        match=f"{missing_name} was not found",
    ) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert browser.screenshot_count == 1


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
        _synthetic_home_ready_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 2
    assert sleeps == [1.0, 1.0, 1.0]
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
        _synthetic_home_ready_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    asyncio.run(screen.before_callback())

    assert len(browser.clicked_points) == 3
    assert sleeps == [1.0, 1.0, 1.0, 1.0]
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
    assert sleeps == [1.0, 1.0]
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
    assert sleeps == [1.0, 1.0]
    assert browser.screenshot_count == 2
    assert exc_info.value.screenshot == mail_screenshot


@pytest.mark.parametrize(
    ("rewards_first", "expected_sleeps"),
    [
        (True, [1.0, 2.0, 0.5, 1.0]),
        (False, [1.0, 1.0, 2.0, 0.5]),
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
        _synthetic_home_ready_screenshot(),
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
    assert sleeps == [1.0, 2.0]
    assert browser.screenshot_count == 2
    assert exc_info.value.screenshot == missing_confirm_screenshot
