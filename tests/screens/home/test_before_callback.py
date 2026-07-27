import asyncio
import logging
from importlib.resources.abc import Traversable
from random import Random

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
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenUnexpectedStateError,
)
from majsoulrpa.screens.home import (
    HomeScreen,
)
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)
from tests.screens.home._support import _synthetic_home_ready_screenshot


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
