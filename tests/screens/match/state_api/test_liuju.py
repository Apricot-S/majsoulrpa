import asyncio
from random import Random
from types import SimpleNamespace

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match import (
    LiujuEvent,
    LiujuType,
    MatchScreen,
)
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


def test_get_state_appends_jiuzhongjiupai_and_clears_operations() -> None:
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
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=1,
                                combination=[],
                            )
                        ]
                    ),
                ),
                _live_liuju_action(step=1, type_=1, seat=0),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 2
    assert state.round.step == 1
    assert state.round.operation_candidates is None
    assert state.round.events[-1] == LiujuEvent(
        action_step=1,
        type=LiujuType.JIUZHONGJIUPAI,
        seat=state.self_seat,
    )
