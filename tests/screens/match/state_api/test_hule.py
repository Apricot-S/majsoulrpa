import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import HuleEvent, MatchScreen
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
    _live_hule_action,
    _live_new_round_action,
)


def test_get_state_applies_self_zimohu() -> None:
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
                    tile="5p",
                    left_tile_count=68,
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[
                            liqi_pb2.OptionalOperation(type=1),
                        ],
                    ),
                ),
                _live_hule_action(
                    step=3,
                    hules=[
                        liqi_pb2.HuleInfo(
                            hand=["1m"] * 13,
                            hu_tile="5p",
                            seat=0,
                            zimo=True,
                            doras=["5p"],
                            fu=30,
                        ),
                    ],
                    old_scores=[25000] * 4,
                    delta_scores=[3000, -1000, -1000, -1000],
                    scores=[28000, 24000, 24000, 24000],
                    doras=[],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 4
    assert state.round.step == 3
    assert state.round.scores == (28000, 24000, 24000, 24000)
    assert state.round.dora_indicators == ("3p",)
    assert state.round.operation_candidates is None
    assert isinstance(state.round.events[-1], HuleEvent)


def test_get_state_applies_tenhou_after_initial_deal() -> None:
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
                    tiles=["1m"] * 13 + ["9s"],
                ),
                _live_hule_action(
                    step=1,
                    hules=[
                        liqi_pb2.HuleInfo(
                            hand=["1m"] * 13,
                            hu_tile="9s",
                            seat=0,
                            zimo=True,
                            qinjia=True,
                            doras=["9s"],
                            fu=30,
                        ),
                    ],
                    old_scores=[25000] * 4,
                    delta_scores=[3000, -1000, -1000, -1000],
                    scores=[28000, 24000, 24000, 24000],
                    doras=["3p"],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert isinstance(state.round.events[-1], HuleEvent)
    assert state.round.events[-1].hules[0].hu_tile == "9s"


def test_get_state_rejects_self_zimohu_with_different_tile() -> None:
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
                    seat=0,
                    tile="5p",
                    left_tile_count=68,
                ),
                _live_hule_action(
                    step=3,
                    hules=[
                        liqi_pb2.HuleInfo(
                            hand=["1m"] * 13,
                            hu_tile="6p",
                            seat=0,
                            zimo=True,
                            doras=["6p"],
                            fu=30,
                        ),
                    ],
                    old_scores=[25000] * 4,
                    delta_scores=[3000, -1000, -1000, -1000],
                    scores=[28000, 24000, 24000, 24000],
                    doras=["3p"],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_zimohu_with_wrong_qinjia() -> None:
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
                    seat=0,
                    tile="5p",
                    left_tile_count=68,
                ),
                _live_hule_action(
                    step=3,
                    hules=[
                        liqi_pb2.HuleInfo(
                            hand=["1m"] * 13,
                            hu_tile="5p",
                            seat=0,
                            zimo=True,
                            qinjia=True,
                            doras=["5p"],
                            fu=30,
                        ),
                    ],
                    old_scores=[25000] * 4,
                    delta_scores=[3000, -1000, -1000, -1000],
                    scores=[28000, 24000, 24000, 24000],
                    doras=["3p"],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())
