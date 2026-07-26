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
    MATCH_RESULT_CONFIRM_SETTINGS_PATH,
    MATCH_RESULT_CONFIRM_TEMPLATE_PATH,
    ROUND_RESULT_CONFIRM_SETTINGS_PATH,
    ROUND_RESULT_CONFIRM_TEMPLATE_PATH,
    SEAT_INDICATOR_SETTINGS_PATH,
    SEAT_INDICATOR_TEMPLATE_PATHS,
)
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import LiujuEvent, MatchScreen, NewRoundEvent
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _request_response,
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


def test_wait_for_state_change_clicks_liuju_and_match_result_confirmations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    confirmation = _synthetic_template_screenshot(
        template_path=LIUJU_CONFIRM_TEMPLATE_PATH,
        settings_path=LIUJU_CONFIRM_SETTINGS_PATH,
    )
    round_result_confirmation = _round_result_confirmation()
    match_result_confirmation = _match_result_confirmation()
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        ".lq.NotifyGameEndResult",
    )
    browser = BrowserControllerSpy(
        confirmation,
        round_result_confirmation,
        match_result_confirmation,
    )
    screen = _screen(browser, messages)
    sleeps: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(terminal))

    assert sleeps == [
        match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS,
    ]
    assert state is None
    assert screen._stale
    assert len(browser.clicked_points) == 3


def test_match_result_wait_puts_back_fetch_room(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    confirmation = _synthetic_template_screenshot(
        template_path=LIUJU_CONFIRM_TEMPLATE_PATH,
        settings_path=LIUJU_CONFIRM_SETTINGS_PATH,
    )
    fetch_room = _request_response(
        ".lq.Lobby.fetchRoom",
        response={"room": {}},
    )
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        ".lq.NotifyGameEndResult",
        fetch_room,
    )
    browser = BrowserControllerSpy(
        confirmation,
        _round_result_confirmation(),
        _synthetic_blank_screenshot(),
    )
    screen = _screen(browser, messages)
    original_sleep = asyncio.sleep

    async def skip_sleep(delay: float) -> None:
        terminal_delay = (
            match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS
        )
        if delay == terminal_delay:
            return
        await original_sleep(delay)

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())
    state = asyncio.run(
        asyncio.wait_for(
            screen.wait_for_state_change(terminal),
            timeout=1.0,
        )
    )

    assert state is None
    assert screen._stale
    assert messages.get_nowait() is fetch_room


def test_wait_for_state_change_clicks_each_hule_confirmation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    confirmation = _synthetic_template_screenshot(
        template_path=HULE_CONFIRM_TEMPLATE_PATH,
        settings_path=HULE_CONFIRM_SETTINGS_PATH,
    )
    round_result_confirmation = _round_result_confirmation()
    match_result_confirmation = _match_result_confirmation()
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
        ".lq.NotifyGameEndResult",
    )
    browser = BrowserControllerSpy(
        confirmation,
        confirmation,
        round_result_confirmation,
        match_result_confirmation,
    )
    screen = _screen(browser, messages)

    async def skip_sleep(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(terminal))

    assert state is None
    assert len(browser.clicked_points) == 4


def test_wait_for_state_change_accepts_confirmation_auto_transition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blank = _synthetic_blank_screenshot()
    next_round_screen = _next_round_screen()
    next_round = _live_new_round_action(step=0, ju=1)
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        next_round,
    )
    browser = BrowserControllerSpy(blank, next_round_screen)
    screen = _screen(browser, messages)
    sleeps: list[float] = []

    async def skip_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(terminal))

    assert state is not None
    assert state.version == terminal.version + 1
    assert state.match_id == terminal.match_id
    assert state.origin == terminal.origin
    assert state.origin_id == terminal.origin_id
    assert state.self_seat == terminal.self_seat
    assert state.players == terminal.players
    assert state.round.generation == terminal.round.generation + 1
    assert state.round.ju == 1
    assert len(state.round.events) == 1
    assert isinstance(state.round.events[0], NewRoundEvent)
    assert state.round.he == ((), (), (), ())
    assert state.round.fulu == ((), (), (), ())
    assert state.round.babei == ((), (), (), ())
    assert state.round.liqi == (False,) * 4
    assert state.round.first_draw == (True,) * 4
    assert state.round.pending_action_target is None
    assert state.round.operation_candidates is None
    assert browser.clicked_points == []
    assert sleeps == [
        match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS,
    ]
    assert messages.get_nowait() is None


def test_wait_for_state_change_rejects_next_round_score_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blank = _synthetic_blank_screenshot()
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        _live_new_round_action(
            step=0,
            ju=1,
            scores=[26000, 25000, 25000, 24000],
        ),
    )
    screen = _screen(
        BrowserControllerSpy(blank, b"inconsistent-screen"),
        messages,
    )

    async def skip_sleep(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.wait_for_state_change(terminal))


def test_wait_for_state_change_waits_for_delayed_confirmation_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blank = _synthetic_blank_screenshot()
    confirmation = _synthetic_template_screenshot(
        template_path=LIUJU_CONFIRM_TEMPLATE_PATH,
        settings_path=LIUJU_CONFIRM_SETTINGS_PATH,
    )
    round_result_confirmation = _round_result_confirmation()
    match_result_confirmation = _match_result_confirmation()
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=0),
        _live_liuju_action(step=1, type_=1, seat=0),
        ".lq.NotifyGameEndResult",
    )
    browser = BrowserControllerSpy(
        blank,
        confirmation,
        round_result_confirmation,
        match_result_confirmation,
    )
    screen = _screen(browser, messages)
    sleeps: list[float] = []

    async def skip_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(terminal))

    assert state is None
    assert len(browser.clicked_points) == 3
    assert sleeps == [
        match_screen_module.TERMINAL_EVENT_SCREEN_DISPLAY_DELAY_SECONDS,
        match_screen_module.OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS,
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
    round_result_confirmation = _round_result_confirmation()
    match_result_confirmation = _match_result_confirmation()
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
        ".lq.NotifyGameEndResult",
    )
    browser = BrowserControllerSpy(
        liuju_confirmation,
        hule_confirmation,
        hule_confirmation,
        round_result_confirmation,
        match_result_confirmation,
    )
    screen = _screen(browser, messages)

    async def skip_sleep(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())
    terminal = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(terminal))

    assert state is None
    assert len(browser.clicked_points) == 5


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


def _round_result_confirmation() -> bytes:
    return _synthetic_template_screenshot(
        template_path=ROUND_RESULT_CONFIRM_TEMPLATE_PATH,
        settings_path=ROUND_RESULT_CONFIRM_SETTINGS_PATH,
    )


def _match_result_confirmation() -> bytes:
    return _synthetic_template_screenshot(
        template_path=MATCH_RESULT_CONFIRM_TEMPLATE_PATH,
        settings_path=MATCH_RESULT_CONFIRM_SETTINGS_PATH,
    )


def _next_round_screen() -> bytes:
    return _synthetic_template_screenshot(
        template_path=SEAT_INDICATOR_TEMPLATE_PATHS[0],
        settings_path=SEAT_INDICATOR_SETTINGS_PATH,
    )
