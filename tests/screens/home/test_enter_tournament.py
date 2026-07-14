import asyncio
import logging

import pytest
from pydantic import JsonValue

import majsoulrpa.screens.home as home_module
from majsoulrpa.assets.templates.home import (
    TOURNAMENT_LOBBY_SETTINGS_PATH,
    TOURNAMENT_LOBBY_TEMPLATE_PATH,
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.assets.templates.home.tournament_lobby import (
    TOURNAMENT_CONFIRM_SETTINGS_PATH,
    TOURNAMENT_CONFIRM_TEMPLATE_PATH,
    TOURNAMENT_ENTER_SETTINGS_PATH,
    TOURNAMENT_ENTER_TEMPLATE_PATH,
    TOURNAMENT_ERROR_CONFIRM_SETTINGS_PATH,
    TOURNAMENT_ERROR_CONFIRM_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenStaleError,
)
from majsoulrpa.screens.home import (
    FETCH_CUSTOMIZED_CONTEST_API_NAME,
    TOURNAMENT_ID_PATTERN,
    EnterTournamentFailureReason,
    HomeScreen,
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


def _tournament_browser(
    *, failure_home_screenshot: bytes | None = None
) -> BrowserControllerSpy:
    screenshots = [
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_MATCH_TEMPLATE_PATH,
            settings_path=TOURNAMENT_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_LOBBY_TEMPLATE_PATH,
            settings_path=TOURNAMENT_LOBBY_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_ENTER_TEMPLATE_PATH,
            settings_path=TOURNAMENT_ENTER_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_CONFIRM_TEMPLATE_PATH,
            settings_path=TOURNAMENT_CONFIRM_SETTINGS_PATH,
        ),
    ]
    if failure_home_screenshot is not None:
        screenshots.append(
            _synthetic_template_screenshot(
                template_path=TOURNAMENT_ERROR_CONFIRM_TEMPLATE_PATH,
                settings_path=TOURNAMENT_ERROR_CONFIRM_SETTINGS_PATH,
            ),
        )
        screenshots.append(failure_home_screenshot)
    return BrowserControllerSpy(screenshots[0], *screenshots[1:])


def test_enter_tournament_failure_reason_has_expected_members() -> None:
    assert list(EnterTournamentFailureReason) == [
        EnterTournamentFailureReason.TOURNAMENT_NOT_FOUND,
        EnterTournamentFailureReason.NO_ACTIVE_SEASON,
        EnterTournamentFailureReason.UNRECOGNIZED_ERROR_CODE,
    ]
    assert EnterTournamentFailureReason.TOURNAMENT_NOT_FOUND.value == 2501
    assert EnterTournamentFailureReason.NO_ACTIVE_SEASON.value == 2536
    assert EnterTournamentFailureReason.UNRECOGNIZED_ERROR_CODE.value == -1


def test_tournament_id_pattern_matches_exactly_six_digits() -> None:
    assert TOURNAMENT_ID_PATTERN.pattern == r"\d{6}"
    assert TOURNAMENT_ID_PATTERN.fullmatch("123456") is not None


def test_enter_tournament_clicks_tournament_match_button(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []
    input_values: list[str] = []
    pressed_keys: list[str] = []

    class TournamentBrowserControllerSpy(BrowserControllerSpy):
        async def input_text(self, text: str) -> None:
            input_values.append(text)
            await super().input_text(text)

        async def press_key(self, key: str) -> None:
            pressed_keys.append(key)
            await super().press_key(key)

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = TournamentBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_MATCH_TEMPLATE_PATH,
            settings_path=TOURNAMENT_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_LOBBY_TEMPLATE_PATH,
            settings_path=TOURNAMENT_LOBBY_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_ENTER_TEMPLATE_PATH,
            settings_path=TOURNAMENT_ENTER_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_CONFIRM_TEMPLATE_PATH,
            settings_path=TOURNAMENT_CONFIRM_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(FETCH_CUSTOMIZED_CONTEST_API_NAME, {}),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO):
        result = asyncio.run(screen.enter_tournament("123456"))

    assert result is None
    assert screen._stale
    assert (
        "screen API called: screen=HomeScreen api=enter_tournament"
        in caplog.text
    )
    assert "123456" not in caplog.text
    assert sleeps == [1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0]
    assert "Entered a tournament successfully." in caplog.messages
    assert len(browser.clicked_points) == 5
    assert browser.screenshot_count == 4
    assert input_values == ["123456"]
    assert pressed_keys == []
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
    enter_region = TemplateMatchSettings.from_toml_file(
        TOURNAMENT_ENTER_SETTINGS_PATH,
    ).region
    x, y = browser.clicked_points[2]
    assert enter_region.left < x < enter_region.left + enter_region.width
    assert enter_region.top < y < enter_region.top + enter_region.height
    x, y = browser.clicked_points[3]
    assert HomeScreen.TOURNAMENT_ID_REGION.left < x
    assert x < HomeScreen.TOURNAMENT_ID_REGION.right
    assert HomeScreen.TOURNAMENT_ID_REGION.top < y
    assert y < HomeScreen.TOURNAMENT_ID_REGION.bottom
    confirm_region = TemplateMatchSettings.from_toml_file(
        TOURNAMENT_CONFIRM_SETTINGS_PATH,
    ).region
    x, y = browser.clicked_points[4]
    assert confirm_region.left < x < confirm_region.left + confirm_region.width
    assert confirm_region.top < y < confirm_region.top + confirm_region.height


def test_enter_tournament_raises_if_fetch_message_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    browser = _tournament_browser()
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(".lq.Unrelated"),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenInconsistentMessageError,
        match=r"fetchCustomizedContestByContestId.*message was not found",
    ):
        asyncio.run(screen.enter_tournament("123456"))

    assert not screen._stale


def test_enter_tournament_raises_if_fetch_response_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    browser = _tournament_browser()
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                FETCH_CUSTOMIZED_CONTEST_API_NAME,
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenInconsistentMessageError,
        match="fetchCustomizedContestByContestId response was not found",
    ):
        asyncio.run(screen.enter_tournament("123456"))

    assert not screen._stale


@pytest.mark.parametrize(
    ("error_code", "expected", "unknown_warning"),
    [
        (2501, EnterTournamentFailureReason.TOURNAMENT_NOT_FOUND, None),
        (2536, EnterTournamentFailureReason.NO_ACTIVE_SEASON, None),
        (
            9999,
            EnterTournamentFailureReason.UNRECOGNIZED_ERROR_CODE,
            (
                "Unrecognized fetchCustomizedContestByContestId "
                "error code: 9999."
            ),
        ),
    ],
)
def test_enter_tournament_returns_failure_reason(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    error_code: int,
    expected: EnterTournamentFailureReason,
    unknown_warning: str | None,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    browser = _tournament_browser(
        failure_home_screenshot=_synthetic_home_ready_screenshot(),
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(
                    FETCH_CUSTOMIZED_CONTEST_API_NAME,
                    {"error": {"code": error_code}},
                ),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO):
        result = asyncio.run(screen.enter_tournament("123456"))

    assert result is expected
    assert not screen._stale
    assert f"Failed to enter a tournament: {expected.name}." in caplog.messages
    assert sleeps == [
        1.0,
        1.0,
        1.0,
        0.5,
        0.5,
        0.5,
        0.5,
        1.0,
        1.0,
    ]
    assert len(browser.clicked_points) == 7
    assert browser.screenshot_count == 6
    error_confirm_region = TemplateMatchSettings.from_toml_file(
        TOURNAMENT_ERROR_CONFIRM_SETTINGS_PATH,
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
    assert HomeScreen.TOURNAMENT_BACK_REGION.left < x
    assert x < HomeScreen.TOURNAMENT_BACK_REGION.right
    assert HomeScreen.TOURNAMENT_BACK_REGION.top < y
    assert y < HomeScreen.TOURNAMENT_BACK_REGION.bottom
    if unknown_warning is None:
        assert (
            "Unrecognized fetchCustomizedContestByContestId error code"
            not in caplog.text
        )
    else:
        assert unknown_warning in caplog.messages


def test_enter_tournament_raises_if_home_buttons_are_missing_after_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    missing_home_screenshot = _synthetic_blank_screenshot()
    browser = _tournament_browser(
        failure_home_screenshot=missing_home_screenshot,
    )
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(
                    FETCH_CUSTOMIZED_CONTEST_API_NAME,
                    {"error": {"code": 2501}},
                ),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="tournament-match was not found",
    ) as exc_info:
        asyncio.run(screen.enter_tournament("123456"))

    assert exc_info.value.screenshot == missing_home_screenshot
    assert not screen._stale


@pytest.mark.parametrize(
    ("response", "message"),
    [
        (
            {"error": {}},
            (
                "fetchCustomizedContestByContestId error must be a dict "
                "containing code"
            ),
        ),
        (
            {"error": "not-a-dict"},
            (
                "fetchCustomizedContestByContestId error must be a dict "
                "containing code"
            ),
        ),
        (
            {"error": {"code": "2501"}},
            "fetchCustomizedContestByContestId error code must be an integer",
        ),
        (
            {"error": {"code": True}},
            "fetchCustomizedContestByContestId error code must be an integer",
        ),
    ],
)
def test_enter_tournament_rejects_inconsistent_error(
    monkeypatch: pytest.MonkeyPatch,
    response: dict[str, JsonValue],
    message: str,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    browser = _tournament_browser()
    screen = HomeScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(
                _request_response(
                    FETCH_CUSTOMIZED_CONTEST_API_NAME,
                    response,
                ),
            ),
        ),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenInconsistentMessageError,
        match=message,
    ):
        asyncio.run(screen.enter_tournament("123456"))

    assert not screen._stale


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


def test_enter_tournament_raises_if_confirm_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    missing_confirm_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_MATCH_TEMPLATE_PATH,
            settings_path=TOURNAMENT_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_LOBBY_TEMPLATE_PATH,
            settings_path=TOURNAMENT_LOBBY_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=TOURNAMENT_ENTER_TEMPLATE_PATH,
            settings_path=TOURNAMENT_ENTER_SETTINGS_PATH,
        ),
        missing_confirm_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="confirm was not found after opening tournament entry dialog",
    ) as exc_info:
        asyncio.run(screen.enter_tournament("123456"))

    assert exc_info.value.screenshot == missing_confirm_screenshot
    assert len(browser.clicked_points) == 3
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


def test_tournament_lobby_button_template_assets_exist() -> None:
    assert TOURNAMENT_LOBBY_TEMPLATE_PATH.name == "tournament-lobby.png"
    assert TOURNAMENT_LOBBY_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_LOBBY_SETTINGS_PATH.name == "tournament-lobby.toml"
    assert TOURNAMENT_LOBBY_SETTINGS_PATH.is_file()


def test_tournament_lobby_dialog_template_assets_exist() -> None:
    assert TOURNAMENT_ENTER_TEMPLATE_PATH.name == "enter.png"
    assert TOURNAMENT_ENTER_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_ENTER_SETTINGS_PATH.name == "enter.toml"
    assert TOURNAMENT_ENTER_SETTINGS_PATH.is_file()
    assert TOURNAMENT_CONFIRM_TEMPLATE_PATH.name == "confirm.png"
    assert TOURNAMENT_CONFIRM_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_CONFIRM_SETTINGS_PATH.name == "confirm.toml"
    assert TOURNAMENT_CONFIRM_SETTINGS_PATH.is_file()
    assert TOURNAMENT_ERROR_CONFIRM_TEMPLATE_PATH.name == "error-confirm.png"
    assert TOURNAMENT_ERROR_CONFIRM_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_ERROR_CONFIRM_SETTINGS_PATH.name == "error-confirm.toml"
    assert TOURNAMENT_ERROR_CONFIRM_SETTINGS_PATH.is_file()
