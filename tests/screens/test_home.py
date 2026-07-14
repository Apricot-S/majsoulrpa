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
from pydantic import JsonValue

import majsoulrpa.screens.home as home_module
from majsoulrpa.assets.templates.home import (
    CREATE_ROOM_SETTINGS_PATH,
    CREATE_ROOM_TEMPLATE_PATH,
    EVENT_CLOSE_SETTINGS_PATH,
    EVENT_CLOSE_TEMPLATE_PATH,
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
    JADE_SETTINGS_PATH,
    JADE_TEMPLATE_PATH,
    JOIN_ROOM_SETTINGS_PATH,
    JOIN_ROOM_TEMPLATE_PATH,
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
    TOURNAMENT_LOBBY_SETTINGS_PATH,
    TOURNAMENT_LOBBY_TEMPLATE_PATH,
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.assets.templates.home.create_room import (
    CREATE_SETTINGS_PATH,
    CREATE_TEMPLATE_PATH,
)
from majsoulrpa.assets.templates.home.join_room import (
    CONFIRM_SETTINGS_PATH,
    CONFIRM_TEMPLATE_PATH,
    ERROR_CONFIRM_SETTINGS_PATH,
    ERROR_CONFIRM_TEMPLATE_PATH,
)
from majsoulrpa.presentation import Region
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
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenStaleError,
    ScreenUnexpectedStateError,
)
from majsoulrpa.screens.home import (
    JOIN_ROOM_API_NAME,
    ROOM_ID_PATTERN,
    TOURNAMENT_ID_PATTERN,
    EnterTournamentFailureReason,
    HomeScreen,
    JoinRoomFailureReason,
    Length,
    Mode,
    ThinkingTime,
)
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
    Direction,
    RawNotice,
    RawRequestResponse,
)
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


def _notice(name: str) -> DecodedNotice:
    return DecodedNotice(
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
    )


def _request_response(
    name: str,
    response: dict[str, JsonValue],
) -> DecodedRequestResponse:
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    return DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=name,
            request=b"synthetic-request",
            response=b"synthetic-response",
            request_observed_at=observed_at,
            response_observed_at=observed_at,
        ),
        request={},
        response=response,
    )


def _message_queue(
    *messages: str | DecodedSnifferMessage,
) -> SnifferMessageQueue:
    queue = SnifferMessageQueue(capacity=10, max_payload_bytes=1024)
    for message in messages:
        queue.enqueue(
            _notice(message) if isinstance(message, str) else message
        )
    return queue


def test_home_screen_is_screen() -> None:
    assert issubclass(HomeScreen, Screen)


def test_inconsistent_message_error_is_runtime_error() -> None:
    assert issubclass(ScreenInconsistentMessageError, RuntimeError)


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


def test_join_room_failure_reason_has_expected_members() -> None:
    assert list(JoinRoomFailureReason) == [
        JoinRoomFailureReason.ROOM_NOT_FOUND,
        JoinRoomFailureReason.ROOM_FULL,
        JoinRoomFailureReason.MATCH_ALREADY_STARTED,
        JoinRoomFailureReason.UNRECOGNIZED_ERROR_CODE,
    ]
    assert JoinRoomFailureReason.ROOM_NOT_FOUND.value == 1100
    assert JoinRoomFailureReason.ROOM_FULL.value == 1101
    assert JoinRoomFailureReason.MATCH_ALREADY_STARTED.value == 1109
    assert JoinRoomFailureReason.UNRECOGNIZED_ERROR_CODE.value == -1


def test_enter_tournament_failure_reason_has_expected_members() -> None:
    assert list(EnterTournamentFailureReason) == [
        EnterTournamentFailureReason.TOURNAMENT_NOT_FOUND,
        EnterTournamentFailureReason.NO_ACTIVE_SEASON,
        EnterTournamentFailureReason.UNRECOGNIZED_ERROR_CODE,
    ]
    assert EnterTournamentFailureReason.TOURNAMENT_NOT_FOUND.value == 2501
    assert EnterTournamentFailureReason.NO_ACTIVE_SEASON.value == 2536
    assert EnterTournamentFailureReason.UNRECOGNIZED_ERROR_CODE.value == -1


def test_room_id_pattern_matches_exactly_five_digits() -> None:
    assert ROOM_ID_PATTERN.pattern == r"\d{5}"
    assert ROOM_ID_PATTERN.fullmatch("12345") is not None


def test_tournament_id_pattern_matches_exactly_six_digits() -> None:
    assert TOURNAMENT_ID_PATTERN.pattern == r"\d{6}"
    assert TOURNAMENT_ID_PATTERN.fullmatch("123456") is not None


def test_enter_tournament_clicks_tournament_match_button(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_MATCH_TEMPLATE_PATH,
            settings_path=TOURNAMENT_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_LOBBY_TEMPLATE_PATH,
            settings_path=TOURNAMENT_LOBBY_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO):
        result = asyncio.run(screen.enter_tournament("123456"))

    assert result is None
    assert not screen._stale
    assert (
        "screen API called: screen=HomeScreen api=enter_tournament"
        in caplog.text
    )
    assert "123456" not in caplog.text
    assert sleeps == [1.0]
    assert len(browser.clicked_points) == 2
    match_region = TemplateMatchSettings.from_toml_file(
        TOURNAMENT_MATCH_SETTINGS_PATH,
    ).region
    x, y = browser.clicked_points[0]
    assert match_region.left < x < match_region.left + match_region.width
    assert match_region.top < y < match_region.top + match_region.height
    lobby_region = TemplateMatchSettings.from_toml_file(
        TOURNAMENT_LOBBY_SETTINGS_PATH,
    ).region
    x, y = browser.clicked_points[1]
    assert lobby_region.left < x < lobby_region.left + lobby_region.width
    assert lobby_region.top < y < lobby_region.top + lobby_region.height


@pytest.mark.parametrize(
    "tournament_id",
    ["", "12345", "1234567", "12345a"],
)
def test_enter_tournament_rejects_id_not_matching_six_digits(
    tournament_id: str,
) -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = HomeScreen(context=ScreenContext(browser=browser))

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="Tournament ID must be exactly 6 digits",
    ) as exc_info:
        asyncio.run(screen.enter_tournament(tournament_id))

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert not screen._stale


def test_enter_tournament_raises_if_tournament_match_button_is_missing() -> (
    None
):
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = HomeScreen(context=ScreenContext(browser=browser))

    with pytest.raises(
        ScreenDetectionError,
        match="tournament-match was not found",
    ) as exc_info:
        asyncio.run(screen.enter_tournament("123456"))

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []
    assert not screen._stale


def test_enter_tournament_raises_if_tournament_lobby_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_lobby_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_MATCH_TEMPLATE_PATH,
            settings_path=TOURNAMENT_MATCH_SETTINGS_PATH,
        ),
        missing_lobby_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="tournament-lobby was not found",
    ) as exc_info:
        asyncio.run(screen.enter_tournament("123456"))

    assert exc_info.value.screenshot == missing_lobby_screenshot
    assert sleeps == [1.0]
    assert len(browser.clicked_points) == 1
    assert not screen._stale


def test_enter_tournament_rejects_stale_home_screen() -> None:
    screenshot = _synthetic_blank_screenshot()
    screen = HomeScreen(
        context=ScreenContext(browser=BrowserControllerSpy(screenshot)),
    )
    screen._mark_stale()

    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(screen.enter_tournament("123456"))

    assert exc_info.value.screenshot == screenshot


def test_join_room_accepts_exactly_five_digits(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    screen = HomeScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(
                _synthetic_template_screenshot(
                    template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
                    settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
                ),
                _synthetic_template_screenshot(
                    template_path=JOIN_ROOM_TEMPLATE_PATH,
                    settings_path=JOIN_ROOM_SETTINGS_PATH,
                ),
                _synthetic_template_screenshot(
                    template_path=CONFIRM_TEMPLATE_PATH,
                    settings_path=CONFIRM_SETTINGS_PATH,
                ),
            ),
            sniffer_messages=_message_queue(
                _request_response(JOIN_ROOM_API_NAME, {}),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO):
        result = asyncio.run(screen.join_room("12345"))

    assert result is None
    assert screen._stale
    assert "screen API called: screen=HomeScreen api=join_room" in caplog.text
    assert "Joined a friendly room successfully." in caplog.text
    assert "12345" not in caplog.text


def test_join_room_raises_if_join_room_response_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    screenshot = _synthetic_template_screenshot(
        template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
        settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(
        screenshot,
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CONFIRM_TEMPLATE_PATH,
            settings_path=CONFIRM_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(JOIN_ROOM_API_NAME),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenInconsistentMessageError,
        match="joinRoom response was not found",
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert exc_info.value.screenshot == screenshot
    assert not screen._stale


@pytest.mark.parametrize(
    ("error_code", "expected", "warning_message"),
    [
        (1100, JoinRoomFailureReason.ROOM_NOT_FOUND, None),
        (1101, JoinRoomFailureReason.ROOM_FULL, None),
        (1109, JoinRoomFailureReason.MATCH_ALREADY_STARTED, None),
        (
            9999,
            JoinRoomFailureReason.UNRECOGNIZED_ERROR_CODE,
            "Unrecognized joinRoom error code: 9999.",
        ),
    ],
)
def test_join_room_returns_failure_reason(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    error_code: int,
    expected: JoinRoomFailureReason,
    warning_message: str | None,
) -> None:
    sleeps: list[float] = []
    timeline: list[str] = []

    class OrderedBrowserControllerSpy(BrowserControllerSpy):
        async def click(self, x: float, y: float) -> None:
            timeline.append("click")
            await super().click(x, y)

        async def screenshot(self) -> bytes:
            timeline.append("screenshot")
            return await super().screenshot()

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        timeline.append(f"sleep:{seconds}")

    browser = OrderedBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CONFIRM_TEMPLATE_PATH,
            settings_path=CONFIRM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=ERROR_CONFIRM_TEMPLATE_PATH,
            settings_path=ERROR_CONFIRM_SETTINGS_PATH,
        ),
        _synthetic_home_ready_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(
                    JOIN_ROOM_API_NAME,
                    {"error": {"code": error_code}},
                ),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO):
        result = asyncio.run(screen.join_room("12345"))

    assert result is expected
    assert not screen._stale
    assert "Joined a friendly room successfully." not in caplog.text
    assert (
        f"Failed to join a friendly room: {expected.name}." in caplog.messages
    )
    assert sleeps == [1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0]
    assert timeline[-7:] == [
        "sleep:0.5",
        "screenshot",
        "click",
        "sleep:1.0",
        "click",
        "sleep:1.0",
        "screenshot",
    ]
    assert len(browser.clicked_points) == 6
    assert browser.screenshot_count == 5
    error_confirm_region = TemplateMatchSettings.from_toml_file(
        ERROR_CONFIRM_SETTINGS_PATH,
    ).region
    x, y = browser.clicked_points[-2]
    assert (
        error_confirm_region.left
        < x
        < error_confirm_region.left + error_confirm_region.width
    )
    assert (
        error_confirm_region.top
        < y
        < error_confirm_region.top + error_confirm_region.height
    )
    x, y = browser.clicked_points[-1]
    assert HomeScreen.JOIN_ROOM_BACK_REGION.left < x
    assert x < HomeScreen.JOIN_ROOM_BACK_REGION.right
    assert HomeScreen.JOIN_ROOM_BACK_REGION.top < y
    assert y < HomeScreen.JOIN_ROOM_BACK_REGION.bottom
    if warning_message is None:
        assert "Unrecognized joinRoom error code" not in caplog.text
    else:
        assert warning_message in caplog.messages


def test_join_room_raises_if_home_buttons_are_missing_after_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    missing_home_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CONFIRM_TEMPLATE_PATH,
            settings_path=CONFIRM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=ERROR_CONFIRM_TEMPLATE_PATH,
            settings_path=ERROR_CONFIRM_SETTINGS_PATH,
        ),
        missing_home_screenshot,
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(
                    JOIN_ROOM_API_NAME,
                    {"error": {"code": 1100}},
                ),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="tournament-match was not found",
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert exc_info.value.screenshot == missing_home_screenshot
    assert not screen._stale


@pytest.mark.parametrize(
    ("response", "message"),
    [
        ({"error": {}}, "joinRoom error must be a dict containing code"),
        (
            {"error": "not-a-dict"},
            "joinRoom error must be a dict containing code",
        ),
        (
            {"error": {"code": "1100"}},
            "joinRoom error code must be an integer",
        ),
        (
            {"error": {"code": True}},
            "joinRoom error code must be an integer",
        ),
    ],
)
def test_join_room_rejects_inconsistent_error(
    monkeypatch: pytest.MonkeyPatch,
    response: dict[str, JsonValue],
    message: str,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    screenshot = _synthetic_template_screenshot(
        template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
        settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(
        screenshot,
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CONFIRM_TEMPLATE_PATH,
            settings_path=CONFIRM_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(JOIN_ROOM_API_NAME, response),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenInconsistentMessageError,
        match=message,
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert exc_info.value.screenshot == screenshot
    assert not screen._stale


def test_join_room_opens_dialog_and_fills_room_id_without_clearing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    timeline: list[str] = []

    class OrderedBrowserControllerSpy(BrowserControllerSpy):
        async def click(self, x: float, y: float) -> None:
            timeline.append("click")
            await super().click(x, y)

        async def screenshot(self) -> bytes:
            timeline.append("screenshot")
            return await super().screenshot()

        async def input_text(self, text: str) -> None:
            timeline.append(f"input:{text}")
            await super().input_text(text)

        async def press_key(self, key: str) -> None:
            timeline.append(f"key:{key}")
            await super().press_key(key)

    async def sleep(seconds: float) -> None:
        timeline.append(f"sleep:{seconds}")

    browser = OrderedBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CONFIRM_TEMPLATE_PATH,
            settings_path=CONFIRM_SETTINGS_PATH,
        ),
    )
    messages = _message_queue(
        ".lq.Unrelated",
        _request_response(JOIN_ROOM_API_NAME, {}),
        ".lq.AfterJoinRoom",
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            rng=Random(0),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    result = asyncio.run(screen.join_room("12345"))

    assert result is None
    assert len(browser.clicked_points) == 4
    x, y = browser.clicked_points[2]
    assert HomeScreen.ROOM_ID_REGION.left < x < HomeScreen.ROOM_ID_REGION.right
    assert HomeScreen.ROOM_ID_REGION.top < y < HomeScreen.ROOM_ID_REGION.bottom
    confirm_region = TemplateMatchSettings.from_toml_file(
        CONFIRM_SETTINGS_PATH,
    ).region
    x, y = browser.clicked_points[3]
    assert confirm_region.left < x < confirm_region.left + confirm_region.width
    assert confirm_region.top < y < confirm_region.top + confirm_region.height
    assert timeline == [
        "screenshot",
        "click",
        "sleep:1.0",
        "screenshot",
        "click",
        "sleep:1.0",
        "screenshot",
        "click",
        "sleep:0.5",
        "input:12345",
        "sleep:0.5",
        "click",
        "sleep:0.5",
    ]
    remaining_message = messages.get_nowait()
    assert remaining_message is not None
    assert remaining_message.raw.name == ".lq.AfterJoinRoom"
    assert messages.get_nowait() is None


def test_join_room_raises_if_join_room_message_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    screenshot = _synthetic_template_screenshot(
        template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
        settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(
        screenshot,
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CONFIRM_TEMPLATE_PATH,
            settings_path=CONFIRM_SETTINGS_PATH,
        ),
    )
    messages = _message_queue(".lq.Unrelated")
    screen = HomeScreen(
        context=ScreenContext(browser=browser, sniffer_messages=messages),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenInconsistentMessageError,
        match=r"\.lq\.Lobby\.joinRoom.*not found",
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert exc_info.value.screenshot == screenshot
    assert messages.get_nowait() is None


def test_join_room_raises_if_friendly_match_button_is_missing() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = HomeScreen(context=ScreenContext(browser=browser))

    with pytest.raises(
        ScreenDetectionError,
        match="friendly-match was not found",
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert browser.clicked_points == []
    assert exc_info.value.screenshot == screenshot


def test_join_room_raises_if_join_room_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_join_room_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        missing_join_room_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="join-room was not found",
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert len(browser.clicked_points) == 1
    assert sleeps == [1.0]
    assert exc_info.value.screenshot == missing_join_room_screenshot


def test_join_room_raises_if_confirm_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_confirm_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=JOIN_ROOM_TEMPLATE_PATH,
            settings_path=JOIN_ROOM_SETTINGS_PATH,
        ),
        missing_confirm_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="confirm was not found after opening room join dialog",
    ) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert len(browser.clicked_points) == 2
    assert sleeps == [1.0, 1.0]
    assert exc_info.value.screenshot == missing_confirm_screenshot


@pytest.mark.parametrize("room_id", ["", "1234", "123456", "12a45"])
def test_join_room_rejects_room_id_not_matching_five_digits(
    room_id: str,
) -> None:
    screenshot = _synthetic_blank_screenshot()
    screen = HomeScreen(
        context=ScreenContext(browser=BrowserControllerSpy(screenshot)),
    )

    with pytest.raises(
        ScreenInvalidArgumentError,
        match="Room ID must be exactly 5 digits",
    ) as exc_info:
        asyncio.run(screen.join_room(room_id))

    assert exc_info.value.screenshot == screenshot


def test_join_room_rejects_stale_home_screen() -> None:
    screenshot = _synthetic_blank_screenshot()
    screen = HomeScreen(
        context=ScreenContext(browser=BrowserControllerSpy(screenshot)),
    )
    screen._mark_stale()

    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(screen.join_room("12345"))

    assert exc_info.value.screenshot == screenshot


def test_mode_regions_have_placeholder_for_each_mode() -> None:
    assert set(HomeScreen.MODE_REGIONS) == set(Mode)
    assert all(
        isinstance(region, Region)
        for region in HomeScreen.MODE_REGIONS.values()
    )


def test_length_regions_have_placeholder_for_each_length() -> None:
    assert set(HomeScreen.LENGTH_REGIONS) == set(Length)
    assert all(
        isinstance(region, Region)
        for region in HomeScreen.LENGTH_REGIONS.values()
    )


def test_thinking_time_regions_have_placeholder_for_each_thinking_time() -> (
    None
):
    assert set(HomeScreen.THINKING_TIME_REGIONS) == set(ThinkingTime)
    assert all(
        isinstance(region, Region)
        for region in HomeScreen.THINKING_TIME_REGIONS.values()
    )


def test_create_room_defaults_to_four_player_two_wind_five_plus_twenty(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    screen = HomeScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(
                _synthetic_template_screenshot(
                    template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
                    settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
                ),
                _synthetic_template_screenshot(
                    template_path=CREATE_ROOM_TEMPLATE_PATH,
                    settings_path=CREATE_ROOM_SETTINGS_PATH,
                ),
                _synthetic_template_screenshot(
                    template_path=CREATE_TEMPLATE_PATH,
                    settings_path=CREATE_SETTINGS_PATH,
                ),
            ),
        ),
    )
    parameters = signature(HomeScreen.create_room).parameters

    assert parameters["mode"].default is Mode.FOUR_PLAYER
    assert parameters["length"].default is Length.TWO_WIND_MATCH
    assert parameters["thinking_time"].default is ThinkingTime.FIVE_PLUS_TWENTY
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        result = asyncio.run(screen.create_room())

    assert result is None
    assert (
        "screen API called: screen=HomeScreen api=create_room" in caplog.text
    )


def test_create_room_accepts_each_enum_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    def create_screen() -> HomeScreen:
        return HomeScreen(
            context=ScreenContext(
                browser=BrowserControllerSpy(
                    _synthetic_template_screenshot(
                        template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
                        settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
                    ),
                    _synthetic_template_screenshot(
                        template_path=CREATE_ROOM_TEMPLATE_PATH,
                        settings_path=CREATE_ROOM_SETTINGS_PATH,
                    ),
                    _synthetic_template_screenshot(
                        template_path=CREATE_TEMPLATE_PATH,
                        settings_path=CREATE_SETTINGS_PATH,
                    ),
                ),
            ),
        )

    async def create_rooms() -> list[None]:
        results = [
            await create_screen().create_room(mode=mode) for mode in Mode
        ]
        results.extend(
            [
                await create_screen().create_room(length=length)
                for length in Length
            ],
        )
        results.extend(
            [
                await create_screen().create_room(thinking_time=thinking_time)
                for thinking_time in ThinkingTime
            ],
        )
        return results

    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    assert asyncio.run(create_rooms()) == [None] * (
        len(Mode) + len(Length) + len(ThinkingTime)
    )


def test_create_room_clicks_settings_then_create_at_half_second_intervals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    timeline: list[str] = []

    class OrderedBrowserControllerSpy(BrowserControllerSpy):
        async def click(self, x: float, y: float) -> None:
            timeline.append("click")
            await super().click(x, y)

        async def screenshot(self) -> bytes:
            timeline.append("screenshot")
            return await super().screenshot()

    async def sleep(seconds: float) -> None:
        timeline.append(f"sleep:{seconds}")

    browser = OrderedBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_ROOM_TEMPLATE_PATH,
            settings_path=CREATE_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_TEMPLATE_PATH,
            settings_path=CREATE_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    result = asyncio.run(screen.create_room())

    assert result is None
    assert screen._stale
    assert len(browser.clicked_points) == 6
    for point, region in zip(
        browser.clicked_points[2:5],
        (
            HomeScreen.MODE_REGIONS[Mode.FOUR_PLAYER],
            HomeScreen.LENGTH_REGIONS[Length.TWO_WIND_MATCH],
            HomeScreen.THINKING_TIME_REGIONS[ThinkingTime.FIVE_PLUS_TWENTY],
        ),
        strict=True,
    ):
        x, y = point
        assert region.left < x < region.right
        assert region.top < y < region.bottom
    assert timeline == [
        "screenshot",
        "click",
        "sleep:1.0",
        "screenshot",
        "click",
        "sleep:1.0",
        "screenshot",
        "click",
        "sleep:0.5",
        "click",
        "sleep:0.5",
        "click",
        "sleep:0.5",
        "click",
    ]


@pytest.mark.parametrize("failing_click_number", [3, 6])
def test_create_room_remains_active_when_setting_or_create_click_fails(
    monkeypatch: pytest.MonkeyPatch,
    failing_click_number: int,
) -> None:
    class FailingBrowserControllerSpy(BrowserControllerSpy):
        def __init__(self, screenshot: bytes, *screenshots: bytes) -> None:
            super().__init__(screenshot, *screenshots)
            self.click_count = 0

        async def click(self, x: float, y: float) -> None:
            self.click_count += 1
            if self.click_count == failing_click_number:
                msg = "synthetic click failure"
                raise RuntimeError(msg)
            await super().click(x, y)

    async def sleep(_seconds: float) -> None:
        pass

    browser = FailingBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_ROOM_TEMPLATE_PATH,
            settings_path=CREATE_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_TEMPLATE_PATH,
            settings_path=CREATE_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(RuntimeError, match="synthetic click failure"):
        asyncio.run(screen.create_room())

    assert not screen._stale


def test_create_room_raises_if_friendly_match_button_is_missing() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = HomeScreen(context=ScreenContext(browser=browser))

    with pytest.raises(
        ScreenDetectionError,
        match="friendly-match was not found",
    ) as exc_info:
        asyncio.run(screen.create_room())

    assert browser.clicked_points == []
    assert exc_info.value.screenshot == screenshot


def test_create_room_raises_if_create_room_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_create_room_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        missing_create_room_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="create-room was not found",
    ) as exc_info:
        asyncio.run(screen.create_room())

    assert len(browser.clicked_points) == 1
    assert sleeps == [1.0]
    assert exc_info.value.screenshot == missing_create_room_screenshot


def test_create_room_raises_if_create_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_create_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_ROOM_TEMPLATE_PATH,
            settings_path=CREATE_ROOM_SETTINGS_PATH,
        ),
        missing_create_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="create was not found after opening room creation",
    ) as exc_info:
        asyncio.run(screen.create_room())

    assert len(browser.clicked_points) == 2
    assert sleeps == [1.0, 1.0]
    assert exc_info.value.screenshot == missing_create_screenshot


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


def test_tournament_lobby_button_template_assets_exist() -> None:
    assert TOURNAMENT_LOBBY_TEMPLATE_PATH.name == "tournament-lobby.png"
    assert TOURNAMENT_LOBBY_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_LOBBY_SETTINGS_PATH.name == "tournament-lobby.toml"
    assert TOURNAMENT_LOBBY_SETTINGS_PATH.is_file()


def test_create_room_template_assets_exist() -> None:
    assert CREATE_ROOM_TEMPLATE_PATH.name == "create-room.png"
    assert CREATE_ROOM_TEMPLATE_PATH.is_file()
    assert CREATE_ROOM_SETTINGS_PATH.name == "create-room.toml"
    assert CREATE_ROOM_SETTINGS_PATH.is_file()


def test_join_room_template_assets_exist() -> None:
    assert JOIN_ROOM_TEMPLATE_PATH.name == "join-room.png"
    assert JOIN_ROOM_TEMPLATE_PATH.is_file()
    assert JOIN_ROOM_SETTINGS_PATH.name == "join-room.toml"
    assert JOIN_ROOM_SETTINGS_PATH.is_file()


def test_join_room_confirm_template_assets_exist() -> None:
    assert CONFIRM_TEMPLATE_PATH.name == "confirm.png"
    assert CONFIRM_TEMPLATE_PATH.is_file()
    assert CONFIRM_SETTINGS_PATH.name == "confirm.toml"
    assert CONFIRM_SETTINGS_PATH.is_file()


def test_join_room_error_confirm_template_assets_exist() -> None:
    assert ERROR_CONFIRM_TEMPLATE_PATH.name == "error-confirm.png"
    assert ERROR_CONFIRM_TEMPLATE_PATH.is_file()
    assert ERROR_CONFIRM_SETTINGS_PATH.name == "error-confirm.toml"
    assert ERROR_CONFIRM_SETTINGS_PATH.is_file()


def test_room_create_button_template_assets_exist() -> None:
    assert CREATE_TEMPLATE_PATH.name == "create.png"
    assert CREATE_TEMPLATE_PATH.is_file()
    assert CREATE_SETTINGS_PATH.name == "create.toml"
    assert CREATE_SETTINGS_PATH.is_file()


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
