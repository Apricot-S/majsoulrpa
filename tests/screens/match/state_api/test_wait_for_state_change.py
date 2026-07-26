import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.screens.errors import ScreenNotImplementedOperationError
from majsoulrpa.screens.match import LiujuEvent, MatchScreen
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_liuju_action,
    _live_new_round_action,
)


def test_wait_for_state_change_returns_terminal_state_before_capture() -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
    )
    browser = BrowserControllerSpy(b"result-screen")
    screen = _screen(browser, messages)
    asyncio.run(screen.before_callback())
    previous = asyncio.run(screen.get_state())
    messages.enqueue(_live_liuju_action(step=1, type_=1, seat=0))

    state = asyncio.run(screen.wait_for_state_change(previous))

    assert state is not None
    assert isinstance(state.round.events[-1], LiujuEvent)
    assert browser.screenshot_count == 0
    assert browser.clicked_points == []


def test_wait_for_state_change_captures_terminal_screen_after_delay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    screenshot = b"result-screen"
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
    )
    browser = BrowserControllerSpy(screenshot)
    screen = _screen(browser, messages)
    sleeps: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    with pytest.raises(ScreenNotImplementedOperationError) as exc_info:
        asyncio.run(screen.wait_for_state_change(terminal))

    assert sleeps == [
        match_screen_module.RESULT_SCREEN_CAPTURE_DELAY_SECONDS,
    ]
    assert exc_info.value.screenshot == screenshot
    assert "LiujuEvent" in str(exc_info.value)
    assert browser.clicked_points == []


def test_get_state_stops_consuming_messages_at_terminal_state() -> None:
    next_round = _live_new_round_action(step=2, ju=1)
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        next_round,
    )
    screen = _screen(BrowserControllerSpy(b"result-screen"), messages)
    asyncio.run(screen.before_callback())

    terminal = asyncio.run(screen.get_state())
    same_terminal = asyncio.run(screen.get_state())

    assert isinstance(terminal.round.events[-1], LiujuEvent)
    assert same_terminal == terminal
    assert messages.get_nowait() is next_round


def _screen(
    browser: BrowserControllerSpy,
    messages: SnifferMessageQueue,
) -> MatchScreen:
    return MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )
