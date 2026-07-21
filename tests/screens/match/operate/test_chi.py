import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match import ChiOperation, MatchScreen
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_discard_action,
    _live_new_round_action,
)


def test_operate_reports_chi_execution_as_not_implemented() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=3,
                    tiles=["3m", "4m", *(["1p"] * 11)],
                ),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="5m",
                    moqie=False,
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=2,
                                combination=["3m|4m"],
                            )
                        ]
                    ),
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    candidates = state.round.operation_candidates
    assert candidates is not None
    [operation] = candidates.operations
    assert isinstance(operation, ChiOperation)

    with pytest.raises(NotImplementedError, match="ChiOperation"):
        asyncio.run(screen.operate(operation))
