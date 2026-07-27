import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import (
    Dapai,
    Jiagang,
    JiagangEvent,
    JiagangOperation,
    MatchScreen,
    validate_seat,
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
    _live_deal_action,
    _live_discard_action,
    _live_jiagang_action,
    _live_new_round_action,
    _live_peng_action,
)


def test_get_state_exposes_jiagang_operation_after_self_draw() -> None:
    tiles = ["0m", "5m", *(["4p"] * 11)]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=2, tiles=tiles),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                ),
                _live_peng_action(
                    step=2,
                    seat=0,
                    tiles=["0m", "5m", "5m"],
                    froms=[0, 0, 2],
                ),
                _live_discard_action(
                    step=3,
                    seat=0,
                    tile="4p",
                    moqie=False,
                ),
                _live_deal_action(
                    step=4,
                    seat=1,
                    tile="",
                    left_tile_count=68,
                ),
                _live_discard_action(
                    step=5,
                    seat=1,
                    tile="2s",
                    moqie=True,
                ),
                _live_deal_action(
                    step=6,
                    seat=0,
                    tile="5m",
                    left_tile_count=67,
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=6,
                                combination=["0m|5m|5m|5m"],
                            )
                        ],
                    ),
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    candidates = state.round.operation_candidates
    assert candidates is not None
    assert candidates.operations == (
        JiagangOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
            added=validate_tile("5m"),
        ),
    )


def test_get_state_applies_self_jiagang_with_drawn_tile() -> None:
    tiles = ["0m", "5m", *(["4p"] * 11)]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=2, tiles=tiles),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                ),
                _live_peng_action(
                    step=2,
                    seat=0,
                    tiles=["0m", "5m", "5m"],
                    froms=[0, 0, 2],
                ),
                _live_discard_action(
                    step=3,
                    seat=0,
                    tile="4p",
                    moqie=False,
                ),
                _live_deal_action(
                    step=4,
                    seat=1,
                    tile="",
                    left_tile_count=68,
                ),
                _live_discard_action(
                    step=5,
                    seat=1,
                    tile="2s",
                    moqie=True,
                ),
                _live_deal_action(
                    step=6,
                    seat=0,
                    tile="5m",
                    left_tile_count=67,
                ),
                _live_jiagang_action(
                    step=7,
                    seat=0,
                    added="5m",
                    doras=["3p", "4p"],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("4p",) * 10
    assert state.round.zimopai is None
    assert state.round.fulu[0] == (
        Jiagang(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
            added=validate_tile("5m"),
        ),
    )
    assert state.round.dora_indicators == ("3p", "4p")
    assert state.round.he[0] == (
        Dapai(
            tile=validate_tile("4p"),
            moqie=False,
            liqi=False,
            wliqi=False,
        ),
    )
    assert state.round.pending_action_target == (0, "5m")
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.lingshang_zimo == (True, False, False, False)
    assert isinstance(state.round.events[-1], JiagangEvent)


def test_get_state_applies_self_jiagang_from_hand() -> None:
    tiles = ["0m", "5m", "5m", *(["4p"] * 10)]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=2, tiles=tiles),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                ),
                _live_peng_action(
                    step=2,
                    seat=0,
                    tiles=["0m", "5m", "5m"],
                    froms=[0, 0, 2],
                ),
                _live_discard_action(
                    step=3,
                    seat=0,
                    tile="4p",
                    moqie=False,
                ),
                _live_deal_action(
                    step=4,
                    seat=1,
                    tile="",
                    left_tile_count=68,
                ),
                _live_discard_action(
                    step=5,
                    seat=1,
                    tile="2s",
                    moqie=True,
                ),
                _live_deal_action(
                    step=6,
                    seat=0,
                    tile="2p",
                    left_tile_count=67,
                ),
                _live_jiagang_action(
                    step=7,
                    seat=0,
                    added="5m",
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("2p", *(("4p",) * 9))
    assert state.round.zimopai is None
    assert state.round.fulu[0] == (
        Jiagang(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
            added=validate_tile("5m"),
        ),
    )


def test_get_state_applies_opponent_jiagang() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=0,
                    tiles=["5m", *(["1m"] * 12)],
                ),
                _live_discard_action(
                    step=1,
                    seat=0,
                    tile="5m",
                    moqie=False,
                ),
                _live_peng_action(
                    step=2,
                    seat=1,
                    tiles=["0m", "5m", "5m"],
                    froms=[1, 1, 0],
                ),
                _live_discard_action(
                    step=3,
                    seat=1,
                    tile="2p",
                    moqie=False,
                ),
                _live_deal_action(
                    step=4,
                    seat=1,
                    tile="",
                    left_tile_count=68,
                ),
                _live_jiagang_action(
                    step=5,
                    seat=1,
                    added="5m",
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("1m",) * 12
    assert state.round.fulu[1] == (
        Jiagang(
            from_seat=validate_seat(0),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
            added=validate_tile("5m"),
        ),
    )
    assert state.round.pending_action_target == (1, "5m")
    assert state.round.lingshang_zimo == (False, True, False, False)


def test_get_state_rejects_jiagang_without_matching_peng() -> None:
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
                _live_jiagang_action(
                    step=3,
                    seat=1,
                    added="5m",
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"
