import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import MatchScreen, NoTileEvent
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
    _live_no_tile_action,
)


def test_get_state_applies_no_tile_score_and_clears_operations() -> None:
    screen = _screen_for_no_tile(
        players=_players(),
        scores=[
            liqi_pb2.NoTileScoreInfo(
                old_scores=[25000] * 4,
                delta_scores=[1500, -1500, 0, 0],
            )
        ],
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 5
    assert state.round.step == 4
    assert state.round.scores == (26500, 23500, 25000, 25000)
    assert state.round.pending_action_target is None
    assert state.round.operation_candidates is None
    assert isinstance(state.round.events[-1], NoTileEvent)


def test_get_state_aggregates_multiple_liujumanguan_score_deltas() -> None:
    screen = _screen_for_no_tile(
        players=_players(),
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
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.scores == (29000, 29000, 21000, 21000)


def test_get_state_keeps_scores_for_empty_no_tile_delta_scores() -> None:
    screen = _screen_for_no_tile(
        players=[
            liqi_pb2.NoTilePlayerInfo(
                tingpai=True,
                hand=["1m"] * 13,
            )
            for _ in range(4)
        ],
        scores=[
            liqi_pb2.NoTileScoreInfo(
                old_scores=[25000] * 4,
                delta_scores=[],
            )
        ],
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.scores == (25000, 25000, 25000, 25000)


def test_get_state_rejects_no_tile_with_wrong_player_count() -> None:
    screen = _screen_for_no_tile(
        players=_players()[:3],
        scores=[
            liqi_pb2.NoTileScoreInfo(
                old_scores=[25000] * 3,
                delta_scores=[],
            )
        ],
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_no_tile_with_wrong_old_scores() -> None:
    screen = _screen_for_no_tile(
        players=_players(),
        scores=[
            liqi_pb2.NoTileScoreInfo(
                old_scores=[24000] * 4,
                delta_scores=[0] * 4,
            )
        ],
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_no_tile_with_inconsistent_liujumanguan() -> None:
    screen = _screen_for_no_tile(
        players=_players(),
        scores=[
            liqi_pb2.NoTileScoreInfo(
                seat=0,
                old_scores=[25000] * 4,
                delta_scores=[8000, -4000, -2000, -2000],
                score=8000,
            )
        ],
        liujumanguan=False,
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_no_tile_before_wall_is_exhausted() -> None:
    screen = _screen_for_no_tile(
        players=_players(),
        scores=[
            liqi_pb2.NoTileScoreInfo(
                old_scores=[25000] * 4,
                delta_scores=[],
            )
        ],
        left_tile_count=1,
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_no_tile_before_final_discard() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
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
                _live_no_tile_action(
                    step=3,
                    players=_players(),
                    scores=[
                        liqi_pb2.NoTileScoreInfo(
                            old_scores=[25000] * 4,
                            delta_scores=[],
                        )
                    ],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def _players() -> list[liqi_pb2.NoTilePlayerInfo]:
    return [
        liqi_pb2.NoTilePlayerInfo(
            tingpai=seat in (0, 2),
            hand=["1m"] * 13 if seat in (0, 2) else [],
        )
        for seat in range(4)
    ]


def _screen_for_no_tile(
    *,
    players: list[liqi_pb2.NoTilePlayerInfo],
    scores: list[liqi_pb2.NoTileScoreInfo],
    liujumanguan: bool = False,
    left_tile_count: int = 0,
) -> MatchScreen:
    return MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
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
                    left_tile_count=left_tile_count,
                ),
                _live_discard_action(
                    step=3,
                    seat=1,
                    tile="8s",
                    moqie=True,
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[
                            liqi_pb2.OptionalOperation(type=9),
                        ]
                    ),
                ),
                _live_no_tile_action(
                    step=4,
                    players=players,
                    scores=scores,
                    liujumanguan=liujumanguan,
                ),
            ),
        ),
    )
