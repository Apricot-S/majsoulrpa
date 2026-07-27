import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.match import (
    MatchScreen,
    ZimoEvent,
)
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
)


def test_get_state_applies_self_draw() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="9s",
                    moqie=False,
                ),
                _live_deal_action(
                    step=2,
                    seat=0,
                    tile="0m",
                    left_tile_count=68,
                    doras=["4p"],
                    liqi=liqi_pb2.LiQiSuccess(
                        seat=3,
                        score=24000,
                        liqibang=1,
                    ),
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 3
    assert state.round.step == 2
    assert state.round.zimopai == "0m"
    assert state.round.left_tile_count == 68
    assert state.round.dora_indicators == ("4p",)
    assert state.round.scores[3] == 24000
    assert state.round.liqibang == 1
    assert state.round.pending_action_target is None
    assert isinstance(state.round.events[-1], ZimoEvent)


def test_get_state_reorders_out_of_step_live_actions() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_deal_action(
                    step=2,
                    seat=0,
                    tile="0m",
                    left_tile_count=68,
                ),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="9s",
                    moqie=False,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 3
    assert state.round.step == 2
    assert isinstance(state.round.events[-1], ZimoEvent)


def test_get_state_continues_after_opponents_concealed_draw() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
                _live_discard_action(
                    step=1,
                    seat=0,
                    tile="1m",
                    moqie=False,
                ),
                _live_deal_action(
                    step=2,
                    seat=1,
                    tile="",
                    left_tile_count=68,
                ),
                _live_discard_action(
                    step=3,
                    seat=1,
                    tile="5p",
                    moqie=True,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.zimopai is None
    assert state.round.dora_indicators == ("3p",)
    assert state.round.pending_action_target == (1, "5p")
    event = state.round.events[-2]
    assert isinstance(event, ZimoEvent)
    assert event.tile is None


def test_get_state_rejects_draw_without_unresolved_discard() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_deal_action(
                    step=1,
                    seat=0,
                    tile="1p",
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


def test_get_state_rejects_draw_with_nonconsecutive_step() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="9s",
                    moqie=False,
                ),
                _live_deal_action(
                    step=3,
                    seat=0,
                    tile="1p",
                    left_tile_count=68,
                ),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="8s",
                    moqie=False,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_draw_over_existing_zimopai() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=1,
                    tiles=["1m"] * 13 + ["9s"],
                ),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="8s",
                    moqie=False,
                ),
                _live_deal_action(
                    step=2,
                    seat=0,
                    tile="1p",
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


@pytest.mark.parametrize(
    ("seat", "tile"),
    [(0, ""), (1, "1p")],
)
def test_get_state_rejects_draw_tile_with_wrong_visibility(
    seat: int,
    tile: str,
) -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="9s",
                    moqie=False,
                ),
                _live_deal_action(
                    step=2,
                    seat=seat,
                    tile=tile,
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"
