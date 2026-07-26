import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import (
    HULE_CONFIRM_SETTINGS_PATH,
    HULE_CONFIRM_TEMPLATE_PATH,
    LIUJU_CONFIRM_SETTINGS_PATH,
    LIUJU_CONFIRM_TEMPLATE_PATH,
)
from majsoulrpa.screens.errors import ScreenNotImplementedOperationError
from majsoulrpa.screens.match import LiujuEvent, MatchScreen
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_deal_action,
    _live_discard_action,
    _live_hule_action,
    _live_liuju_action,
    _live_new_round_action,
    _live_no_tile_action,
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


def test_wait_for_state_change_clicks_liuju_confirmation_before_capture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    confirmation = _synthetic_template_screenshot(
        template_path=LIUJU_CONFIRM_TEMPLATE_PATH,
        settings_path=LIUJU_CONFIRM_SETTINGS_PATH,
    )
    result_screen = b"result-screen"
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
    )
    browser = BrowserControllerSpy(confirmation, result_screen)
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
        match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS,
        match_screen_module.SCORE_RESULT_SCREEN_DISPLAY_DELAY_SECONDS,
    ]
    assert exc_info.value.screenshot == result_screen
    assert "LiujuEvent" in str(exc_info.value)
    assert len(browser.clicked_points) == 1


def test_wait_for_state_change_clicks_each_hule_confirmation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    confirmation = _synthetic_template_screenshot(
        template_path=HULE_CONFIRM_TEMPLATE_PATH,
        settings_path=HULE_CONFIRM_SETTINGS_PATH,
    )
    result_screen = b"result-screen"
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            ju=0,
            tiles=["1m"] * 13 + ["9s"],
        ),
        _live_discard_action(
            step=1,
            seat=0,
            tile="9s",
            moqie=False,
        ),
        _live_hule_action(
            step=2,
            hules=[
                _rong_hule(seat=1),
                _rong_hule(seat=2),
            ],
            old_scores=[25000] * 4,
            delta_scores=[-8000, 4000, 4000, 0],
            scores=[17000, 29000, 29000, 25000],
            doras=[],
        ),
    )
    browser = BrowserControllerSpy(
        confirmation,
        confirmation,
        result_screen,
    )
    screen = _screen(browser, messages)

    async def skip_sleep(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    with pytest.raises(ScreenNotImplementedOperationError) as exc_info:
        asyncio.run(screen.wait_for_state_change(terminal))

    assert exc_info.value.screenshot == result_screen
    assert len(browser.clicked_points) == 2


def test_wait_for_state_change_accepts_confirmation_auto_transition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blank = _synthetic_blank_screenshot()
    result_screen = b"result-screen"
    next_round = _live_new_round_action(step=0, ju=1)
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        next_round,
    )
    browser = BrowserControllerSpy(blank, result_screen)
    screen = _screen(browser, messages)
    sleeps: list[float] = []

    async def skip_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    with pytest.raises(ScreenNotImplementedOperationError) as exc_info:
        asyncio.run(screen.wait_for_state_change(terminal))

    assert exc_info.value.screenshot == result_screen
    assert browser.clicked_points == []
    assert sleeps == [
        match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS,
        match_screen_module.SCORE_RESULT_SCREEN_DISPLAY_DELAY_SECONDS,
    ]
    assert messages.get_nowait() is next_round


def test_wait_for_state_change_waits_for_delayed_confirmation_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blank = _synthetic_blank_screenshot()
    confirmation = _synthetic_template_screenshot(
        template_path=LIUJU_CONFIRM_TEMPLATE_PATH,
        settings_path=LIUJU_CONFIRM_SETTINGS_PATH,
    )
    result_screen = b"result-screen"
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
    )
    browser = BrowserControllerSpy(blank, confirmation, result_screen)
    screen = _screen(browser, messages)
    sleeps: list[float] = []

    async def skip_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    with pytest.raises(ScreenNotImplementedOperationError) as exc_info:
        asyncio.run(screen.wait_for_state_change(terminal))

    assert exc_info.value.screenshot == result_screen
    assert len(browser.clicked_points) == 1
    assert sleeps == [
        match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS,
        match_screen_module.OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS,
        match_screen_module.SCORE_RESULT_SCREEN_DISPLAY_DELAY_SECONDS,
    ]


def test_wait_for_state_change_advances_liujumanguan_presentations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    liuju_confirmation = _synthetic_template_screenshot(
        template_path=LIUJU_CONFIRM_TEMPLATE_PATH,
        settings_path=LIUJU_CONFIRM_SETTINGS_PATH,
    )
    hule_confirmation = _synthetic_template_screenshot(
        template_path=HULE_CONFIRM_TEMPLATE_PATH,
        settings_path=HULE_CONFIRM_SETTINGS_PATH,
    )
    result_screen = b"result-screen"
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0),
        _live_discard_action(
            step=1,
            seat=3,
            tile="9s",
            moqie=False,
        ),
        _live_deal_action(
            step=2,
            seat=1,
            tile="",
            left_tile_count=0,
        ),
        _live_discard_action(
            step=3,
            seat=1,
            tile="8s",
            moqie=True,
        ),
        _live_no_tile_action(
            step=4,
            players=[
                liqi_pb2.NoTilePlayerInfo(
                    tingpai=seat in (0, 2),
                    hand=["1m"] * 13 if seat in (0, 2) else [],
                )
                for seat in range(4)
            ],
            scores=[
                liqi_pb2.NoTileScoreInfo(
                    seat=0,
                    old_scores=[25000] * 4,
                    delta_scores=[8000, -4000, -2000, -2000],
                    score=8000,
                ),
                liqi_pb2.NoTileScoreInfo(
                    seat=1,
                    old_scores=[25000] * 4,
                    delta_scores=[-4000, 8000, -2000, -2000],
                    score=8000,
                ),
            ],
            liujumanguan=True,
        ),
    )
    browser = BrowserControllerSpy(
        liuju_confirmation,
        hule_confirmation,
        hule_confirmation,
        result_screen,
    )
    screen = _screen(browser, messages)

    async def skip_sleep(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    with pytest.raises(ScreenNotImplementedOperationError) as exc_info:
        asyncio.run(screen.wait_for_state_change(terminal))

    assert exc_info.value.screenshot == result_screen
    assert len(browser.clicked_points) == 3


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


def _rong_hule(*, seat: int) -> liqi_pb2.HuleInfo:
    return liqi_pb2.HuleInfo(
        hand=["1m"] * 13,
        hu_tile="9s",
        seat=seat,
        fu=30,
    )
