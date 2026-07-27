import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.match import (
    Chi,
    ChiEvent,
    DapaiOperation,
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
    _live_chi_action,
    _live_discard_action,
    _live_new_round_action,
)


def test_get_state_applies_self_chi() -> None:
    tiles = ["2m", "3m", *(["4p"] * 11)]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=3, tiles=tiles),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="1m",
                    moqie=False,
                ),
                _live_chi_action(
                    step=2,
                    seat=0,
                    tiles=["2m", "3m", "1m"],
                    froms=[0, 0, 3],
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[liqi_pb2.OptionalOperation(type=1)],
                    ),
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 3
    assert state.round.step == 2
    assert state.round.shoupai == ("4p",) * 11
    assert state.round.fulu[0] == (
        Chi(
            from_seat=validate_seat(3),
            tile=validate_tile("1m"),
            consumed=(validate_tile("2m"), validate_tile("3m")),
        ),
    )
    assert state.round.pending_action_target is None
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.operation_candidates is not None
    assert state.round.operation_candidates.operations == (
        DapaiOperation(tile=validate_tile("4p"), moqie=False),
    )
    event = state.round.events[-1]
    assert isinstance(event, ChiEvent)
    assert event.tile == "1m"
    assert event.consumed == ("2m", "3m")


def test_get_state_applies_opponent_chi_and_liqi_success() -> None:
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
                    tile="1m",
                    moqie=False,
                    liqi=True,
                ),
                _live_chi_action(
                    step=2,
                    seat=2,
                    tiles=["2m", "3m", "1m"],
                    froms=[2, 2, 1],
                    liqi=liqi_pb2.LiQiSuccess(
                        seat=1,
                        score=24000,
                        liqibang=1,
                    ),
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("1m",) * 13
    assert state.round.fulu[2] == (
        Chi(
            from_seat=validate_seat(1),
            tile=validate_tile("1m"),
            consumed=(validate_tile("2m"), validate_tile("3m")),
        ),
    )
    assert state.round.scores[1] == 24000
    assert state.round.liqibang == 1
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.pending_action_target is None
    assert state.round.operation_candidates is None


@pytest.mark.parametrize(
    ("step", "from_seat", "chi_tiles", "shoupai"),
    [
        (3, 3, ["2m", "3m", "1m"], ["2m", "3m", *(["4p"] * 11)]),
        (2, 2, ["2m", "3m", "1m"], ["2m", "3m", *(["4p"] * 11)]),
        (2, 3, ["2m", "3m", "4m"], ["2m", "3m", *(["4p"] * 11)]),
        (2, 3, ["2m", "3m", "1m"], ["1m"] * 13),
    ],
)
def test_get_state_rejects_inconsistent_self_chi(
    step: int,
    from_seat: int,
    chi_tiles: list[str],
    shoupai: list[str],
) -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=3, tiles=shoupai),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="1m",
                    moqie=False,
                ),
                _live_chi_action(
                    step=step,
                    seat=0,
                    tiles=chi_tiles,
                    froms=[0, 0, from_seat],
                ),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="1m",
                    moqie=False,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


def test_get_state_rejects_chi_in_three_player_match() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(player_count=3),
                _live_new_round_action(
                    step=0,
                    ju=2,
                    scores=[35000] * 3,
                    tiles=["2m", "3m", *(["4p"] * 11)],
                ),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="1m",
                    moqie=False,
                ),
                _live_chi_action(
                    step=2,
                    seat=0,
                    tiles=["2m", "3m", "1m"],
                    froms=[0, 0, 2],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())
