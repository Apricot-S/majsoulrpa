import asyncio
import logging
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenInvalidOperationError,
    ScreenStaleError,
)
from majsoulrpa.screens.match import (
    DapaiEvent,
    DapaiOperation,
    MatchScreen,
    MatchState,
    validate_tile,
)
from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _notice,
    _request_response,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
)


class _MessagesOnClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        messages: SnifferMessageQueue,
        *messages_on_click: DecodedSnifferMessage,
    ) -> None:
        super().__init__(b"synthetic-screenshot")
        self._messages = messages
        self._messages_on_click = messages_on_click

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        await super().click(x, y, warp=warp)
        for message in self._messages_on_click:
            self._messages.enqueue(message)


class _MessagesByClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        messages: SnifferMessageQueue,
        *messages_by_click: tuple[DecodedSnifferMessage, ...],
    ) -> None:
        super().__init__(b"synthetic-screenshot")
        self._messages = messages
        self._messages_by_click = list(messages_by_click)

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        await super().click(x, y, warp=warp)
        if not self._messages_by_click:
            return
        for message in self._messages_by_click.pop(0):
            self._messages.enqueue(message)


def test_operate_discards_dealers_presented_fourteenth_tile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            tiles=["1m"] * 13 + ["9s"],
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[liqi_pb2.OptionalOperation(type=1)],
            ),
        ),
    )
    browser = _MessagesOnClickBrowser(
        messages,
        _live_discard_action(
            step=1,
            seat=0,
            tile="9s",
            moqie=False,
        ),
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )
    sleep_delays: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operation = next(
        operation
        for operation in candidates.operations
        if operation.tile == validate_tile("9s")
    )

    state = asyncio.run(screen.operate(operation))

    assert operation.moqie is False
    assert state.version == initial.version + 1
    assert state.round.events[-1] == DapaiEvent(
        action_step=1,
        seat=state.self_seat,
        tile=validate_tile("9s"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )
    assert sleep_delays == [2.0]
    [(x, y)] = browser.clicked_points
    assert 1495 < x < 1566
    assert 936 < y < 1040
    assert len(browser.moved_points) == 2
    safe_x, safe_y = browser.moved_points[1]
    assert 585 < safe_x < 1585
    assert 790 < safe_y < 860


@pytest.mark.parametrize(
    ("moqie", "expected_left"),
    [(False, 232), (True, 1495)],
)
def test_operate_distinguishes_hand_and_drawn_tile(
    *,
    moqie: bool,
    expected_left: int,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=1),
        _live_discard_action(step=1, seat=3, tile="9s", moqie=False),
        _live_deal_action(
            step=2,
            seat=0,
            tile="1m",
            left_tile_count=68,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[liqi_pb2.OptionalOperation(type=1)],
            ),
        ),
    )
    browser = _MessagesOnClickBrowser(
        messages,
        _live_discard_action(
            step=3,
            seat=0,
            tile="1m",
            moqie=moqie,
        ),
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
    assert state.round.operation_candidates is not None
    operation = DapaiOperation(tile=validate_tile("1m"), moqie=moqie)

    state = asyncio.run(screen.operate(operation))

    assert state.round.events[-1].action_step == 3
    [(x, y)] = browser.clicked_points
    assert expected_left < x < expected_left + 71
    assert 936 < y < 1040


def test_operate_rejects_when_no_candidate_exists() -> None:
    browser = BrowserControllerSpy(b"no-candidate-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(step=0),
            ),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInvalidOperationError) as exc_info:
        asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("1m"), moqie=False),
            )
        )

    assert exc_info.value.screenshot == b"no-candidate-screenshot"
    assert browser.clicked_points == []


def test_operate_rejects_operation_outside_current_candidates() -> None:
    browser = BrowserControllerSpy(b"invalid-operation-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    tiles=["1m"] * 13 + ["9s"],
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[
                            liqi_pb2.OptionalOperation(
                                type=1,
                                combination=["9s"],
                            )
                        ],
                    ),
                ),
            ),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInvalidArgumentError) as exc_info:
        asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("9s"), moqie=False),
            )
        )

    assert exc_info.value.screenshot == b"invalid-operation-screenshot"
    assert browser.clicked_points == []


def test_operate_drains_messages_before_validating_candidate() -> None:
    browser = BrowserControllerSpy(b"expired-operation-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
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

    with pytest.raises(ScreenInvalidOperationError):
        asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("9s"), moqie=False),
            )
        )

    state = asyncio.run(screen.get_state())
    assert state.version == 2
    assert browser.clicked_points == []


@pytest.mark.parametrize(
    ("seat", "tile"),
    [(0, "1m"), (1, "9s")],
)
def test_operate_rejects_unexpected_state_event(
    monkeypatch: pytest.MonkeyPatch,
    *,
    seat: int,
    tile: str,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            tiles=["1m"] * 13 + ["9s"],
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[liqi_pb2.OptionalOperation(type=1)],
            ),
        ),
    )
    browser = _MessagesOnClickBrowser(
        messages,
        _live_discard_action(
            step=1,
            seat=seat,
            tile=tile,
            moqie=False,
        ),
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("9s"), moqie=False),
            )
        )

    assert exc_info.value.screenshot == b"synthetic-screenshot"
    assert asyncio.run(screen.get_state()).version == 2


def test_operate_rejects_stale_screen_without_clicking() -> None:
    browser = BrowserControllerSpy(b"stale-screenshot")
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(
                _auth_game(),
                _live_new_round_action(
                    step=0,
                    operation=liqi_pb2.OptionalOperationList(
                        operation_list=[liqi_pb2.OptionalOperation(type=1)],
                    ),
                ),
            ),
        ),
    )
    asyncio.run(screen.before_callback())
    asyncio.run(screen.reload())

    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("1m"), moqie=False),
            )
        )

    assert exc_info.value.screenshot == b"stale-screenshot"
    assert browser.clicked_points == []


@pytest.mark.parametrize(
    "input_name",
    [".lq.FastTest.inputOperation", ".lq.FastTest.inputChiPengGang"],
)
def test_operate_puts_back_input_progress_and_logs_only_outer_screen_api(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    input_name: str,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            tiles=["1m"] * 13 + ["9s"],
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[liqi_pb2.OptionalOperation(type=1)],
            ),
        ),
    )
    browser = _MessagesOnClickBrowser(
        messages,
        _request_response(input_name, {}),
        _live_discard_action(
            step=1,
            seat=0,
            tile="9s",
            moqie=False,
        ),
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())

    with caplog.at_level(logging.INFO):
        asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("9s"), moqie=False),
            )
        )

    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == [
        "screen API called: screen=MatchScreen api=operate"
    ]
    assert any(
        f'"name":"{input_name}"' in record.getMessage()
        for record in caplog.records
    )


def test_operate_retries_click_until_input_progresses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            tiles=["1m"] * 13 + ["9s"],
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[liqi_pb2.OptionalOperation(type=1)],
            ),
        ),
    )
    browser = _MessagesByClickBrowser(
        messages,
        (),
        (
            _request_response(".lq.FastTest.inputOperation", {}),
            _live_discard_action(
                step=1,
                seat=0,
                tile="9s",
                moqie=False,
            ),
        ),
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    monkeypatch.setattr(
        match_screen_module,
        "DAPAI_CLICK_RETRY_INTERVAL_SECONDS",
        0.001,
        raising=False,
    )
    asyncio.run(screen.before_callback())

    async def operate_with_deadline() -> MatchState:
        async with asyncio.timeout(0.05):
            return await screen.operate(
                DapaiOperation(tile=validate_tile("9s"), moqie=False),
            )

    state = asyncio.run(operate_with_deadline())

    assert state.version == 2
    assert len(browser.clicked_points) == 2


def test_operate_processes_common_message_before_retrying(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            tiles=["1m"] * 13 + ["9s"],
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[liqi_pb2.OptionalOperation(type=1)],
            ),
        ),
    )
    browser = _MessagesByClickBrowser(
        messages,
        (_notice(".lq.Lobby.fetchServerTime"),),
        (
            _request_response(".lq.FastTest.inputOperation", {}),
            _live_discard_action(
                step=1,
                seat=0,
                tile="9s",
                moqie=False,
            ),
        ),
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)
    asyncio.run(screen.before_callback())

    with caplog.at_level(logging.INFO):
        state = asyncio.run(
            screen.operate(
                DapaiOperation(tile=validate_tile("9s"), moqie=False),
            )
        )

    assert state.version == 2
    assert len(browser.clicked_points) == 2
    assert any(
        '"name":".lq.Lobby.fetchServerTime"' in record.getMessage()
        for record in caplog.records
    )
