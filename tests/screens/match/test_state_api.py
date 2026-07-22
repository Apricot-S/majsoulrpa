import asyncio
import logging
from dataclasses import FrozenInstanceError
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
    ScreenUnexpectedStateError,
)
from majsoulrpa.screens.match import (
    Angang,
    AngangEvent,
    Chi,
    ChiEvent,
    ChiOperation,
    Daminggang,
    DaminggangEvent,
    DaminggangOperation,
    Dapai,
    DapaiEvent,
    DapaiOperation,
    MatchOrigin,
    MatchRank,
    MatchScreen,
    NewRoundEvent,
    Peng,
    PengEvent,
    PengOperation,
    StartMatchEvent,
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
    _live_action,
    _live_angang_action,
    _live_chi_action,
    _live_daminggang_action,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
    _live_peng_action,
)


def _replace_events(value: object, name: str) -> None:
    setattr(value, name, ())


def test_get_state_exposes_initial_match_events() -> None:
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    messages = _message_queue(
        _auth_game(),
        _live_action(),
        _live_new_round_action(step=1),
        ".lq.Lobby.fetchServerTime",
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.version == 1
    assert state.match_id == "synthetic-match-id"
    assert state.origin is MatchOrigin.FRIENDLY
    assert state.origin_id == 12345
    assert state.self_seat == 0
    assert len(state.players) == 4
    assert state.players[0].level4 == MatchRank(id=10101, score=0)
    assert state.players[0].level3 == MatchRank(id=20101, score=10)
    assert state.round.events[0] == StartMatchEvent(action_step=0)
    assert isinstance(state.round.events[1], NewRoundEvent)
    assert state.round.events[1].action_step == 1
    with pytest.raises(FrozenInstanceError):
        _replace_events(state.round, "events")
    assert messages.get_nowait() is None
    assert browser.events == ["move_mouse"]


def test_get_state_starts_events_with_new_round_without_mj_start() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert len(state.round.events) == 1
    assert isinstance(state.round.events[0], NewRoundEvent)
    assert state.round.events[0].action_step == 0


def test_get_state_normalizes_observed_cpu_metadata() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(
                    cpu_count=3,
                    seat_list=(1, SELF_ACCOUNT_ID, 2, 3),
                ),
                _live_new_round_action(step=0),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.self_seat == 1
    assert state.players[1].account_id == SELF_ACCOUNT_ID
    for seat, account_id in ((0, 1), (2, 2), (3, 3)):
        player = state.players[seat]
        assert player.seat == seat
        assert player.is_cpu
        assert player.account_id == account_id
        assert player.name == ""
        assert player.level4 == MatchRank(id=10101, score=0)
        assert player.level3 == MatchRank(id=20101, score=0)


def test_get_state_normalizes_vs_ai_cpu_seats_without_robot_metadata() -> None:
    auth_game = _auth_game(
        cpu_count=3,
        seat_list=(102, SELF_ACCOUNT_ID, 101, 103),
    )
    auth_game.response["robots"] = []
    auth_game.response["ready_id_list"] = [102, 101, 103]
    auth_game.response["is_game_start"] = False
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                auth_game,
                _live_new_round_action(step=0),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.self_seat == 1
    assert state.players[1].account_id == SELF_ACCOUNT_ID
    for seat, account_id in ((0, 102), (2, 101), (3, 103)):
        player = state.players[seat]
        assert player.seat == seat
        assert player.is_cpu
        assert player.account_id == account_id
        assert player.name == ""
        assert player.level4 == MatchRank(id=10101, score=0)
        assert player.level3 == MatchRank(id=20101, score=0)


def test_match_screen_rejects_missing_robot_metadata_outside_vs_ai() -> None:
    auth_game = _auth_game(
        cpu_count=3,
        seat_list=(102, SELF_ACCOUNT_ID, 101, 103),
    )
    auth_game.response["robots"] = []
    auth_game.response["ready_id_list"] = [102, 101]
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(auth_game),
        ),
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


def test_match_screen_rejects_metadata_without_supported_origin() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"unsupported-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(room_id=0, contest_uid=0),
            ),
        ),
    )

    with pytest.raises(ScreenUnexpectedStateError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == b"unsupported-screenshot"


def test_match_screen_rejects_nonzero_mode_id_for_friendly_match() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(mode_id=1),
            ),
        ),
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


def test_initial_state_accepts_auth_game_after_initial_actions() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _live_action(),
                _live_new_round_action(step=1),
                _auth_game(),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.events[0] == StartMatchEvent(action_step=0)
    assert isinstance(state.round.events[1], NewRoundEvent)


def test_get_state_logs_only_screen_and_api_name(
    caplog: pytest.LogCaptureFixture,
) -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
            ),
        ),
    )
    asyncio.run(screen.before_callback())
    caplog.clear()

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(screen.get_state())

    [record] = [
        record
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert record.message == (
        "screen API called: screen=MatchScreen api=get_state"
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
    assert state.round.previous_dapai_seat == 0
    assert state.round.previous_dapai_tile == "9s"
    assert isinstance(state.round.events[-1], DapaiEvent)
    assert state.round.events[-1].action_step == 2


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


def test_get_state_applies_self_draw() -> None:
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
                    tile="0m",
                    left_tile_count=68,
                    doras=["4p"],
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

    assert state.version == 3
    assert state.round.step == 2
    assert state.round.zimopai == "0m"
    assert state.round.left_tile_count == 68
    assert state.round.dora_indicators == ("4p",)
    assert state.round.scores[3] == 24000
    assert state.round.liqibang == 1
    assert state.round.previous_dapai_seat is None
    assert state.round.previous_dapai_tile is None
    assert isinstance(state.round.events[-1], ZimoEvent)


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
    assert state.round.previous_dapai_seat is None
    assert state.round.previous_dapai_tile is None
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
    assert state.round.previous_dapai_seat is None
    assert state.round.operation_candidates is None


def test_get_state_applies_self_peng() -> None:
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
        Peng(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
        ),
    )
    assert state.round.previous_dapai_seat is None
    assert state.round.previous_dapai_tile is None
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.operation_candidates is not None
    assert state.round.operation_candidates.operations == (
        DapaiOperation(tile=validate_tile("4p"), moqie=False),
    )
    assert isinstance(state.round.events[-1], PengEvent)


def test_get_state_applies_opponent_peng_and_liqi_success() -> None:
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
                _live_peng_action(
                    step=2,
                    seat=1,
                    tiles=["5m", "5m", "5m"],
                    froms=[1, 1, 3],
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
        Peng(
            from_seat=validate_seat(3),
            tile=validate_tile("5m"),
            consumed=(validate_tile("5m"), validate_tile("5m")),
        ),
    )
    assert state.round.scores[3] == 24000
    assert state.round.liqibang == 1
    assert state.round.first_draw == (False,) * 4
    assert state.round.yifa == (False,) * 4
    assert state.round.previous_dapai_seat is None
    assert state.round.operation_candidates is None


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
    assert state.round.previous_dapai_seat is None
    assert state.round.previous_dapai_tile is None
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
    assert state.round.previous_dapai_seat is None
    assert state.round.previous_dapai_tile is None
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
    assert state.round.previous_dapai_seat is None
    assert state.round.previous_dapai_tile is None
    assert state.round.previous_qianggang_seat == 0
    assert state.round.previous_qianggang_tile == "0m"
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
    assert state.round.previous_qianggang_seat == 1
    assert state.round.previous_qianggang_tile == "7z"


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

    assert state.round.previous_qianggang_seat is None
    assert state.round.previous_qianggang_tile is None
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
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


@pytest.mark.parametrize(
    ("step", "from_seat", "peng_tiles", "shoupai"),
    [
        (3, 2, ["5m", "5m", "5m"], ["5m", "5m", *(["4p"] * 11)]),
        (2, 3, ["5m", "5m", "5m"], ["5m", "5m", *(["4p"] * 11)]),
        (2, 2, ["6m", "6m", "6m"], ["6m", "6m", *(["4p"] * 11)]),
        (2, 2, ["5m", "5m", "5m"], ["1m"] * 13),
    ],
)
def test_get_state_rejects_inconsistent_self_peng(
    step: int,
    from_seat: int,
    peng_tiles: list[str],
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
                _live_peng_action(
                    step=step,
                    seat=0,
                    tiles=peng_tiles,
                    froms=[0, 0, from_seat],
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


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


def test_get_state_continues_after_opponents_concealed_draw() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
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
                _live_discard_action(
                    step=3,
                    seat=1,
                    tile="5p",
                    moqie=True,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.zimopai is None
    assert state.round.dora_indicators == ("3p",)
    assert state.round.previous_dapai_seat == 1
    assert state.round.previous_dapai_tile == "5p"
    event = state.round.events[-2]
    assert isinstance(event, ZimoEvent)
    assert event.tile is None


def test_get_state_rejects_draw_without_unresolved_discard() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0, ju=1),
                _live_deal_action(
                    step=1,
                    seat=0,
                    tile="1p",
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


def test_get_state_rejects_draw_with_nonconsecutive_step() -> None:
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
                    step=3,
                    seat=0,
                    tile="1p",
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


def test_get_state_rejects_draw_over_existing_zimopai() -> None:
    screen = MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"inconsistent-screenshot"),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    ju=1,
                    tiles=["1m"] * 13 + ["9s"],
                ),
                _live_discard_action(
                    step=1,
                    seat=3,
                    tile="8s",
                    moqie=False,
                ),
                _live_deal_action(
                    step=2,
                    seat=0,
                    tile="1p",
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.get_state())


@pytest.mark.parametrize(
    ("seat", "tile"),
    [(0, ""), (1, "1p")],
)
def test_get_state_rejects_draw_tile_with_wrong_visibility(
    seat: int,
    tile: str,
) -> None:
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
                    seat=seat,
                    tile=tile,
                    left_tile_count=68,
                ),
            ),
        ),
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


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
