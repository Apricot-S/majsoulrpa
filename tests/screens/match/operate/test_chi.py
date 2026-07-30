import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import CHI_TEMPLATE_PATH
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import (
    ChiEvent,
    ChiOperation,
    DaminggangEvent,
    HuleEvent,
    MatchScreen,
    MatchState,
    PengEvent,
)
from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _synthetic_blank_screenshot,
    _synthetic_template_at_screenshot,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_chi_action,
    _live_daminggang_action,
    _live_discard_action,
    _live_hule_action,
    _live_new_round_action,
    _live_peng_action,
)


class _MessagesOnClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        *messages_on_click: DecodedSnifferMessage,
    ) -> None:
        super().__init__(screenshot)
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
        screenshot: bytes,
        messages: SnifferMessageQueue,
        *messages_by_click: tuple[DecodedSnifferMessage, ...],
    ) -> None:
        super().__init__(screenshot)
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
        for message in self._messages_by_click.pop(0):
            self._messages.enqueue(message)


class _PutBackTrackingQueue(SnifferMessageQueue):
    def __init__(self) -> None:
        super().__init__(capacity=10, max_payload_bytes=1024)
        self.put_back_count = 0

    def put_back(self, message: DecodedSnifferMessage) -> None:
        self.put_back_count += 1
        super().put_back(message)


class _MessageOnScreenshotBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        message_on_screenshot: DecodedSnifferMessage,
    ) -> None:
        super().__init__(screenshot)
        self._messages = messages
        self._message_on_screenshot: DecodedSnifferMessage | None = (
            message_on_screenshot
        )

    async def screenshot(self) -> bytes:
        if self._message_on_screenshot is not None:
            self._messages.enqueue(self._message_on_screenshot)
            self._message_on_screenshot = None
        return await super().screenshot()


@pytest.mark.parametrize(
    ("candidate_count", "index", "expected_left"),
    [
        (2, 0, 761),
        (2, 1, 961),
        (3, 1, 861),
        (4, 3, 1161),
        (5, 0, 461),
        (5, 4, 1261),
    ],
)
def test_chi_peng_combination_regions_follow_candidate_layout(
    candidate_count: int,
    index: int,
    expected_left: int,
) -> None:
    region = MatchScreen._get_chi_peng_combination_region(
        candidate_count,
        index,
    )

    assert region.left == expected_left
    assert region.top == 692
    assert region.width == 157
    assert region.height == 117


def test_operate_selects_only_chi_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
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
    )
    screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_chi_action(
            step=2,
            seat=0,
            tiles=["3m", "4m", "5m"],
            froms=[0, 0, 3],
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
        item
        for item in candidates.operations
        if isinstance(item, ChiOperation)
    )
    assert isinstance(operation, ChiOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    assert isinstance(state.round.events[-1], ChiEvent)
    assert sleep_delays == [1.5]
    [(x, y)] = browser.clicked_points
    assert 900 < x < 1050
    assert 650 < y < 688


def test_operate_selects_requested_chi_from_multiple_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=[
                "3m",
                "4m",
                "4m",
                "6m",
                "6m",
                "7m",
                *(["1p"] * 7),
            ],
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
                        combination=["3m|4m", "4m|6m", "6m|7m"],
                    )
                ]
            ),
        ),
    )
    screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (
            _live_chi_action(
                step=2,
                seat=0,
                tiles=["4m", "6m", "5m"],
                froms=[0, 0, 3],
            ),
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
    operation = candidates.operations[1]
    assert isinstance(operation, ChiOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    event = state.round.events[-1]
    assert isinstance(event, ChiEvent)
    assert event.consumed == operation.consumed
    assert sleep_delays == [0.4, 1.5]
    assert len(browser.clicked_points) == 2
    selection_x, selection_y = browser.clicked_points[1]
    assert 861 < selection_x < 1018
    assert 692 < selection_y < 809


def test_operate_accepts_opponent_peng_preemption_after_click(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
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
    )
    screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_peng_action(
            step=2,
            seat=1,
            tiles=["5m", "5m", "5m"],
            froms=[1, 1, 3],
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

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operation = next(
        item
        for item in candidates.operations
        if isinstance(item, ChiOperation)
    )
    assert isinstance(operation, ChiOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    assert isinstance(state.round.events[-1], PengEvent)
    assert state.round.events[-1].seat == 1


def test_operate_accepts_opponent_daminggang_preemption_after_click(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
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
    )
    screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_daminggang_action(
            step=2,
            seat=1,
            tiles=["5m", "5m", "5m", "5m"],
            froms=[1, 1, 1, 3],
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

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operation = next(
        item
        for item in candidates.operations
        if isinstance(item, ChiOperation)
    )
    assert isinstance(operation, ChiOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    assert isinstance(state.round.events[-1], DaminggangEvent)
    assert state.round.events[-1].seat == 1


def test_operate_does_not_click_combination_after_peng_preemption(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _PutBackTrackingQueue()
    for message in (
        _auth_game(),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=[
                "3m",
                "4m",
                "4m",
                "6m",
                "6m",
                "7m",
                *(["1p"] * 7),
            ],
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
                        combination=["3m|4m", "4m|6m", "6m|7m"],
                    )
                ]
            ),
        ),
    ):
        messages.enqueue(message)
    screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_peng_action(
            step=2,
            seat=1,
            tiles=["5m", "5m", "5m"],
            froms=[1, 1, 3],
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

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operation = candidates.operations[1]
    assert isinstance(operation, ChiOperation)

    state = asyncio.run(screen.operate(operation))

    assert isinstance(state.round.events[-1], PengEvent)
    assert messages.put_back_count == 1
    assert len(browser.clicked_points) == 1


@pytest.mark.parametrize(
    ("preempting_action", "expected_event_type"),
    [
        (
            _live_peng_action(
                step=2,
                seat=1,
                tiles=["5m", "5m", "5m"],
                froms=[1, 1, 3],
            ),
            PengEvent,
        ),
        (
            _live_daminggang_action(
                step=2,
                seat=1,
                tiles=["5m", "5m", "5m", "5m"],
                froms=[1, 1, 1, 3],
            ),
            DaminggangEvent,
        ),
        (
            _live_hule_action(
                step=2,
                hules=[
                    liqi_pb2.HuleInfo(
                        hand=["1m"] * 13,
                        hu_tile="5m",
                        seat=1,
                        fu=30,
                    )
                ],
                old_scores=[25000] * 4,
                delta_scores=[0, 8000, 0, -8000],
                scores=[25000, 33000, 25000, 17000],
                doras=[],
            ),
            HuleEvent,
        ),
    ],
)
def test_operate_puts_back_preemption_while_waiting_for_chi_button(
    monkeypatch: pytest.MonkeyPatch,
    preempting_action: DecodedSnifferMessage,
    expected_event_type: type[PengEvent | DaminggangEvent | HuleEvent],
) -> None:
    messages = _PutBackTrackingQueue()
    for message in (
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
    ):
        messages.enqueue(message)
    browser = _MessageOnScreenshotBrowser(
        _synthetic_blank_screenshot(),
        messages,
        preempting_action,
    )
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )
    monkeypatch.setattr(
        match_screen_module,
        "OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS",
        0.001,
    )

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operation = next(
        item
        for item in candidates.operations
        if isinstance(item, ChiOperation)
    )
    assert isinstance(operation, ChiOperation)

    async def operate_with_deadline() -> MatchState:
        async with asyncio.timeout(0.1):
            return await screen.operate(operation)

    state = asyncio.run(operate_with_deadline())

    assert isinstance(state.round.events[-1], expected_event_type)
    assert messages.put_back_count == 1
    assert browser.clicked_points == []


def test_operate_retries_until_chi_button_is_drawn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
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
    )
    button_screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        button_screenshot,
        messages,
        _live_chi_action(
            step=2,
            seat=0,
            tiles=["3m", "4m", "5m"],
            froms=[0, 0, 3],
        ),
    )
    browser.screenshot_queue = [
        _synthetic_blank_screenshot(),
        button_screenshot,
    ]
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
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    operation = next(
        item
        for item in state.round.operation_candidates.operations
        if isinstance(item, ChiOperation)
    )

    result = asyncio.run(screen.operate(operation))

    assert isinstance(result.round.events[-1], ChiEvent)
    assert sleep_delays == [0.2, 1.5]


def test_operate_rejects_chi_event_for_different_combination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=["3m", "4m", "4m", "6m", *(["1p"] * 9)],
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
    )
    screenshot = _synthetic_template_at_screenshot(
        template_path=CHI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_chi_action(
            step=2,
            seat=0,
            tiles=["4m", "6m", "5m"],
            froms=[0, 0, 3],
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

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    operation = next(
        item
        for item in state.round.operation_candidates.operations
        if isinstance(item, ChiOperation)
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.operate(operation))

    assert exc_info.value.screenshot == screenshot


def test_operate_does_not_succeed_without_button_or_preemption(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
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
    )
    browser = BrowserControllerSpy(_synthetic_blank_screenshot())
    screen = MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )
    monkeypatch.setattr(
        match_screen_module,
        "OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS",
        0.001,
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    operation = next(
        item
        for item in state.round.operation_candidates.operations
        if isinstance(item, ChiOperation)
    )

    async def operate_with_deadline() -> None:
        async with asyncio.timeout(0.05):
            await screen.operate(operation)

    with pytest.raises(TimeoutError):
        asyncio.run(operate_with_deadline())

    assert browser.clicked_points == []
