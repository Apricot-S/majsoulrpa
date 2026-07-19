import asyncio
import logging
from random import Random

import pytest

from majsoulrpa.presentation import Region
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import MatchScreen, StartMatchEvent
from majsoulrpa.screens.match import screen as match_screen_module
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import OBSERVED_AT, _live_action


def test_match_screen_before_callback_moves_mouse_away_from_hand() -> None:
    assert (
        Region(left=585, top=790, width=1000, height=70)
        == MatchScreen.MOUSE_SAFE_REGION
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            sniffer_messages=_message_queue(_live_action()),
        ),
    )

    asyncio.run(screen.before_callback())

    [(x, y)] = browser.moved_points
    assert 585 < x < 1585
    assert 790 < y < 860
    assert browser.events == ["move_mouse"]
    assert screen._start_match_event == StartMatchEvent(
        action_step=0,
        observed_at=OBSERVED_AT,
    )


def test_match_screen_logs_only_special_message_levels(
    caplog: pytest.LogCaptureFixture,
) -> None:
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            sniffer_messages=_message_queue(
                ".lq.Lobby.fetchServerTime",
                ".lq.Lobby.heatbeat",
                ".lq.Lobby.loginBeat",
                _live_action(),
            ),
        ),
    )

    with caplog.at_level(logging.DEBUG):
        asyncio.run(screen.before_callback())

    levels = {
        next(
            name
            for name in (
                ".lq.Lobby.fetchServerTime",
                ".lq.Lobby.heatbeat",
                ".lq.Lobby.loginBeat",
                "ActionMJStart",
            )
            if name in record.message
        ): record.levelno
        for record in caplog.records
        if record.name == "majsoulrpa.screens.match.screen"
    }
    assert levels[".lq.Lobby.fetchServerTime"] == logging.INFO
    assert levels[".lq.Lobby.heatbeat"] == logging.DEBUG
    assert levels[".lq.Lobby.loginBeat"] == logging.WARNING
    assert levels["ActionMJStart"] == logging.INFO
    action_log = next(
        record.message
        for record in caplog.records
        if "ActionMJStart" in record.message
    )
    assert '"data"' not in action_log


def test_match_screen_rejects_unknown_initialization_message() -> None:
    browser = BrowserControllerSpy(b"inconsistent-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            sniffer_messages=_message_queue(".lq.Unknown"),
        ),
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"
    assert browser.events == ["move_mouse", "screenshot"]


def test_match_screen_requires_action_mj_start_at_step_zero() -> None:
    browser = BrowserControllerSpy(b"inconsistent-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            sniffer_messages=_message_queue(_live_action(step=1)),
        ),
    )

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.before_callback())


def test_match_screen_initialization_times_out_with_screenshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        match_screen_module,
        "MATCH_INITIALIZATION_TIMEOUT_SECONDS",
        0.0,
    )
    browser = BrowserControllerSpy(b"timeout-screenshot")
    screen = MatchScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == b"timeout-screenshot"
    assert browser.events == ["move_mouse", "screenshot"]
