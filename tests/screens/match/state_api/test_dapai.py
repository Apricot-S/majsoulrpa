import asyncio
from random import Random
from types import SimpleNamespace

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match import (
    Dapai,
    DapaiEvent,
    MatchScreen,
    RongOperation,
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
    _live_action,
    _live_discard_action,
    _live_new_round_action,
)


def test_get_state_applies_dealers_first_discard() -> None:
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_action(),
                _live_new_round_action(
                    step=1,
                    tiles=["1m"] * 13 + ["9s"],
                ),
                _live_discard_action(
                    step=2,
                    seat=0,
                    tile="9s",
                    moqie=False,
                    doras=["4p"],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 2
    assert state.round.step == 2
    assert state.round.shoupai == ("1m",) * 13
    assert state.round.zimopai is None
    assert state.round.dora_indicators == ("4p",)
    assert state.round.he[0] == (
        Dapai(
            tile=validate_tile("9s"),
            moqie=False,
            liqi=False,
            wliqi=False,
        ),
    )
    assert state.round.first_draw[0] is False
    assert state.round.pending_action_target == (0, "9s")
    assert isinstance(state.round.events[-1], DapaiEvent)
    assert state.round.events[-1].action_step == 2


def test_get_state_materializes_rong_candidate_from_discard() -> None:
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
                    seat=1,
                    tile="0m",
                    moqie=False,
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=9,
                                combination=[],
                            )
                        ]
                    ),
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.operation_candidates is not None
    assert state.round.operation_candidates.operations == (
        RongOperation(
            from_seat=validate_seat(1),
            tile=validate_tile("0m"),
        ),
    )
