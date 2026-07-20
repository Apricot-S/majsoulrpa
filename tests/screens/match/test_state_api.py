import asyncio
import logging
from dataclasses import FrozenInstanceError
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.screens.match import (
    MatchOrigin,
    MatchScreen,
    NewRoundEvent,
    StartMatchEvent,
)
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_action,
    _live_new_round_action,
)


def _replace_events(value: object, name: str) -> None:
    setattr(value, name, ())


def test_get_state_exposes_initial_match_events() -> None:
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    messages = _message_queue(
        _auth_game(),
        _live_action(),
        _live_new_round_action(step=1),
        ".lq.Lobby.fetchServerTime",
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 1
    assert state.match_id == "synthetic-match-id"
    assert state.origin is MatchOrigin.FRIENDLY
    assert state.origin_id == 12345
    assert state.self_seat == 0
    assert len(state.players) == 4
    assert state.round.events[0] == StartMatchEvent(action_step=0)
    assert isinstance(state.round.events[1], NewRoundEvent)
    assert state.round.events[1].action_step == 1
    with pytest.raises(FrozenInstanceError):
        _replace_events(state.round, "events")
    assert messages.get_nowait() is None
    assert browser.events == ["move_mouse"]


def test_get_state_starts_events_with_new_round_without_mj_start() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert len(state.round.events) == 1
    assert isinstance(state.round.events[0], NewRoundEvent)
    assert state.round.events[0].action_step == 0


def test_initial_state_accepts_auth_game_after_initial_actions() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _live_action(),
                _live_new_round_action(step=1),
                _auth_game(),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.events[0] == StartMatchEvent(action_step=0)
    assert isinstance(state.round.events[1], NewRoundEvent)


def test_get_state_logs_only_screen_and_api_name(
    caplog: pytest.LogCaptureFixture,
) -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
            ),
        ),
    )
    asyncio.run(screen.before_callback())
    caplog.clear()

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(screen.get_state())

    [record] = [
        record
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert record.message == (
        "screen API called: screen=MatchScreen api=get_state"
    )
