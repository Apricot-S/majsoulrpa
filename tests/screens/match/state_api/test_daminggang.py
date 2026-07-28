import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.match import (
    Daminggang,
    DaminggangEvent,
    MatchScreen,
    ZimoEvent,
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
    _live_daminggang_action,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
)


def test_get_state_applies_self_daminggang() -> None:
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
                _live_daminggang_action(
                    step=2,
                    seat=0,
                    tiles=["0m", "5m", "5m", "5m"],
                    froms=[0, 0, 0, 2],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 3
    assert state.round.step == 2
    assert state.round.shoupai == ("4p",) * 10
    assert state.round.fulu[0] == (
        Daminggang(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("0m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
    )
    assert state.round.pending_action_target is None
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.lingshang_zimo == (True, False, False, False)
    assert state.round.operation_candidates is None
    assert isinstance(state.round.events[-1], DaminggangEvent)


def test_get_state_applies_opponent_daminggang_and_liqi_success() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=3),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="5m",
                    moqie=False,
                    liqi=True,
                ),
                _live_daminggang_action(
                    step=2,
                    seat=1,
                    tiles=["5m", "5m", "5m", "5m"],
                    froms=[1, 1, 1, 3],
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

    assert state.round.shoupai == ("1m",) * 13
    assert state.round.fulu[1] == (
        Daminggang(
            from_seat=validate_seat(3),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("5m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
    )
    assert state.round.scores[3] == 24000
    assert state.round.liqibang == 1
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.lingshang_zimo == (False, True, False, False)
    assert state.round.pending_action_target is None
    assert state.round.operation_candidates is None


def test_get_state_applies_lingshang_draw_after_daminggang() -> None:
    tiles = ["5m", "5m", "5m", *(["4p"] * 10)]
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
                _live_daminggang_action(
                    step=2,
                    seat=0,
                    tiles=["5m", "5m", "5m", "5m"],
                    froms=[0, 0, 0, 2],
                ),
                _live_deal_action(
                    step=3,
                    seat=0,
                    tile="1p",
                    left_tile_count=67,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.step == 3
    assert state.round.zimopai == "1p"
    assert state.round.lingshang_zimo == (True, False, False, False)
    assert isinstance(state.round.events[-1], ZimoEvent)


def test_get_state_rejects_repeated_opponent_lingshang_draw() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=3),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="5m",
                    moqie=False,
                ),
                _live_daminggang_action(
                    step=2,
                    seat=1,
                    tiles=["5m", "5m", "5m", "5m"],
                    froms=[1, 1, 1, 3],
                ),
                _live_deal_action(
                    step=3,
                    seat=1,
                    tile="",
                    left_tile_count=67,
                ),
                _live_deal_action(
                    step=4,
                    seat=1,
                    tile="",
                    left_tile_count=66,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


@pytest.mark.parametrize(
    ("step", "from_seat", "gang_tiles", "shoupai"),
    [
        (3, 2, ["5m"] * 4, ["5m", "5m", "5m", *(["4p"] * 10)]),
        (2, 3, ["5m"] * 4, ["5m", "5m", "5m", *(["4p"] * 10)]),
        (2, 2, ["6m"] * 4, ["6m", "6m", "6m", *(["4p"] * 10)]),
        (2, 2, ["5m"] * 4, ["1m"] * 13),
    ],
)
def test_get_state_rejects_inconsistent_self_daminggang(
    step: int,
    from_seat: int,
    gang_tiles: list[str],
    shoupai: list[str],
) -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=2, tiles=shoupai),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                ),
                _live_daminggang_action(
                    step=step,
                    seat=0,
                    tiles=gang_tiles,
                    froms=[0, 0, 0, from_seat],
                ),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"
