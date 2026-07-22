import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.match import (
    Angang,
    AngangEvent,
    MatchScreen,
    validate_tile,
)
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_angang_action,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
)


def test_get_state_applies_self_angang_with_drawn_tile() -> None:
    tiles = ["0m", "5m", "5m", *(["4p"] * 10)]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1, tiles=tiles),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="1s",
                    moqie=False,
                ),
                _live_deal_action(
                    step=2,
                    seat=0,
                    tile="5m",
                    left_tile_count=68,
                ),
                _live_angang_action(
                    step=3,
                    seat=0,
                    tile="5m",
                    doras=["3p", "4p"],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    consumed = (
        validate_tile("0m"),
        validate_tile("5m"),
        validate_tile("5m"),
        validate_tile("5m"),
    )
    assert state.round.shoupai == ("4p",) * 10
    assert state.round.zimopai is None
    assert state.round.fulu[0] == (Angang(consumed=consumed),)
    assert state.round.dora_indicators == ("3p", "4p")
    assert state.round.he[0] == ()
    assert state.round.previous_dapai is None
    assert state.round.previous_qianggang == (0, "0m")
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.lingshang_zimo == (True, False, False, False)
    assert isinstance(state.round.events[-1], AngangEvent)


def test_get_state_applies_red_normalized_angang_to_black_fives() -> None:
    tiles = ["5m"] * 4 + ["4p"] * 10
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=0, tiles=tiles),
                _live_angang_action(step=1, seat=0, tile="5m"),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("4p",) * 10
    assert state.round.zimopai is None
    assert state.round.fulu[0][0] == Angang(
        consumed=(
            validate_tile("0m"),
            validate_tile("5m"),
            validate_tile("5m"),
            validate_tile("5m"),
        )
    )


def test_get_state_applies_opponent_angang() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_angang_action(step=1, seat=1, tile="7z"),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("1m",) * 13
    assert state.round.zimopai is None
    assert state.round.fulu[1] == (
        Angang(
            consumed=(
                validate_tile("7z"),
                validate_tile("7z"),
                validate_tile("7z"),
                validate_tile("7z"),
            )
        ),
    )
    assert state.round.previous_qianggang == (1, "7z")


def test_get_state_clears_qianggang_target_on_lingshang_draw() -> None:
    tiles = ["1z"] * 4 + ["4p"] * 10
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=0, tiles=tiles),
                _live_angang_action(step=1, seat=0, tile="1z"),
                _live_deal_action(
                    step=2,
                    seat=0,
                    tile="2p",
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.previous_qianggang is None
    assert state.round.zimopai == "2p"


def test_get_state_rejects_self_angang_without_four_tiles() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=0,
                    tiles=["1z", *(["4p"] * 13)],
                ),
                _live_angang_action(step=1, seat=0, tile="1z"),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"
