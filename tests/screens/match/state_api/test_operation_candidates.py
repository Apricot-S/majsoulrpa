import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.match import (
    AngangOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    MatchScreen,
    PengOperation,
    SkipOperation,
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
    _live_new_round_action,
)


def test_get_state_exposes_chi_operations_after_opponent_discard() -> None:
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
                    tile="0m",
                    moqie=False,
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=2,
                                combination=["3m|4m"],
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
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("0m"),
            consumed=(validate_tile("3m"), validate_tile("4m")),
        ),
        SkipOperation(),
    )


def test_get_state_exposes_peng_operations_after_opponent_discard() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=2,
                    tiles=["0m", "5m", *(["1p"] * 11)],
                ),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=3,
                                combination=["0m|5m"],
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
        PengOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
        ),
        SkipOperation(),
    )


def test_get_state_exposes_daminggang_after_opponent_discard() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=2,
                    tiles=["0m", "5m", "5m", *(["1p"] * 10)],
                ),
                _live_discard_action(
                    step=1,
                    seat=2,
                    tile="5m",
                    moqie=False,
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=5,
                                combination=["0m|5m|5m"],
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
        DaminggangOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("0m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
        SkipOperation(),
    )


def test_get_state_rejects_chi_operation_in_three_player_match() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(
                    player_count=3,
                    seat_list=(100002, SELF_ACCOUNT_ID, 100003),
                ),
                _live_new_round_action(
                    step=0,
                    ju=0,
                    scores=[35000] * 3,
                    tiles=["3m", "4m", *(["1p"] * 11)],
                ),
                _live_discard_action(
                    step=1,
                    seat=0,
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
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_exposes_initial_dapai_operation_candidates() -> None:
    tiles = [
        "0m",
        "5m",
        "1p",
        "1p",
        "2p",
        "3p",
        "4p",
        "5p",
        "6p",
        "7p",
        "8p",
        "9p",
        "1z",
        "2z",
    ]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    tiles=tiles,
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=1,
                                combination=["5m"],
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
    assert candidates.time_fixed_ms == 5000
    assert candidates.time_add_ms == 20000
    assert candidates.operations == tuple(
        DapaiOperation(tile=validate_tile(tile), moqie=False)
        for tile in (
            "1p",
            "2p",
            "3p",
            "4p",
            "5p",
            "6p",
            "7p",
            "8p",
            "9p",
            "1z",
            "2z",
        )
    )


def test_get_state_exposes_initial_angang_operation_candidate() -> None:
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
                    tiles=["1z"] * 4 + ["2m"] * 10,
                    operation=liqi_pb2.OptionalOperationList(
                        time_fixed=5000,
                        time_add=20000,
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=4,
                                combination=["1z|1z|1z|1z"],
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
        AngangOperation(
            consumed=(
                validate_tile("1z"),
                validate_tile("1z"),
                validate_tile("1z"),
                validate_tile("1z"),
            )
        ),
    )


def test_get_state_distinguishes_hand_and_drawn_dapai_operations() -> None:
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
                    tile="1m",
                    left_tile_count=68,
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

    candidates = state.round.operation_candidates
    assert candidates is not None
    assert candidates.operations == (
        DapaiOperation(tile=validate_tile("1m"), moqie=False),
        DapaiOperation(tile=validate_tile("1m"), moqie=True),
    )


def test_get_state_clears_previous_operation_candidates() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    tiles=["1m"] * 13 + ["9s"],
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[liqi_pb2.OptionalOperation(type=1)],
                    ),
                ),
                _live_discard_action(
                    step=1,
                    seat=0,
                    tile="9s",
                    moqie=False,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    initial = screen._state_store.state
    assert initial is not None
    assert initial.round.operation_candidates is not None

    state = asyncio.run(screen.get_state())

    assert state.round.operation_candidates is None
