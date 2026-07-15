import asyncio
import logging
from random import Random

import pytest
from pydantic import JsonValue

import majsoulrpa.screens.home as home_module
from majsoulrpa.assets.templates.home import (
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
    JOIN_ROOM_SETTINGS_PATH,
    JOIN_ROOM_TEMPLATE_PATH,
)
from majsoulrpa.assets.templates.home.join_room import (
    CONFIRM_SETTINGS_PATH,
    CONFIRM_TEMPLATE_PATH,
    ERROR_CONFIRM_SETTINGS_PATH,
    ERROR_CONFIRM_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenStaleError,
)
from majsoulrpa.screens.home import (
    JOIN_ROOM_API_NAME,
    ROOM_ID_PATTERN,
    HomeScreen,
    JoinRoomFailureReason,
)
from tests.screens.home._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _request_response,
    _synthetic_blank_screenshot,
    _synthetic_home_ready_screenshot,
    _synthetic_template_screenshot,
)


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


def test_room_id_pattern_matches_exactly_five_digits() -> None:
    assert ROOM_ID_PATTERN.pattern == r"\d{5}"
    assert ROOM_ID_PATTERN.fullmatch("12345") is not None


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
    assert "Sniffer message:" not in caplog.text
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
        async def click(
            self,
            x: float,
            y: float,
            *,
            warp: bool = False,
        ) -> None:
            timeline.append("click")
            await super().click(x, y, warp=warp)

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
    messages = _message_queue(
        _request_response(
            JOIN_ROOM_API_NAME,
            {"error": {"code": error_code}},
        ),
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO):
        result = asyncio.run(screen.join_room("12345"))

    assert result is expected
    assert not screen._stale
    assert "Joined a friendly room successfully." not in caplog.text
    assert "Sniffer message:" in caplog.text
    assert JOIN_ROOM_API_NAME in caplog.text
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
    assert messages.get_nowait() is None


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
        async def click(
            self,
            x: float,
            y: float,
            *,
            warp: bool = False,
        ) -> None:
            timeline.append("click")
            await super().click(x, y, warp=warp)

        async def screenshot(self) -> bytes:
            timeline.append("screenshot")
            return await super().screenshot()

        async def input_text(self, text: str) -> None:
            timeline.append(f"input:{text}")
            await super().input_text(text)

        async def press_key(self, key: str) -> None:
            timeline.append(f"key:{key}")
            await super().press_key(key)

    class OrderedHomeScreen(HomeScreen):
        def _mark_stale(self) -> None:
            timeline.append("mark_stale")
            super()._mark_stale()

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
    screen = OrderedHomeScreen(
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
        "sleep:1.0",
        "mark_stale",
    ]
    remaining_message = messages.get_nowait()
    assert remaining_message is not None
    assert remaining_message.raw.name == JOIN_ROOM_API_NAME
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
