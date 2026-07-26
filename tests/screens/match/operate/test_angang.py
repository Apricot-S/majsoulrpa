import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import GANG_TEMPLATE_PATH
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
    ScreenNotImplementedOperationError,
)
from majsoulrpa.screens.match import AngangEvent, AngangOperation, MatchScreen
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
    _live_angang_action,
    _live_new_round_action,
)


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
        if not self._messages_by_click:
            return
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


def _angang_message_sequence(
    combinations: list[str],
    tiles: list[str],
) -> tuple[DecodedSnifferMessage, ...]:
    return (
        _auth_game(),
        _live_new_round_action(
            step=0,
            ju=0,
            tiles=tiles,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=4,
                        combination=combinations,
                    )
                ]
            ),
        ),
    )


def _angang_messages(
    combinations: list[str],
    tiles: list[str],
) -> SnifferMessageQueue:
    return _message_queue(*_angang_message_sequence(combinations, tiles))


def _screen(
    browser: BrowserControllerSpy,
    messages: SnifferMessageQueue,
) -> MatchScreen:
    return MatchScreen(
        context=ScreenContext(
            browser=browser,
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=messages,
        ),
    )


def _gang_button_screenshot() -> bytes:
    return _synthetic_template_at_screenshot(
        template_path=GANG_TEMPLATE_PATH,
        left=900,
        top=650,
    )


def test_operate_selects_only_angang_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _angang_messages(
        ["1z|1z|1z|1z"],
        [*("1z" for _ in range(4)), *("2m" for _ in range(10))],
    )
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (_live_angang_action(step=1, seat=0, tile="1z"),),
    )
    screen = _screen(browser, messages)
    sleep_delays: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    [operation] = candidates.operations
    assert isinstance(operation, AngangOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    event = state.round.events[-1]
    assert isinstance(event, AngangEvent)
    assert event.consumed == operation.consumed
    assert sleep_delays == [1.5]
    [(x, y)] = browser.clicked_points
    assert 900 < x < 1050
    assert 650 < y < 688


def test_operate_retries_until_gang_button_is_drawn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _angang_messages(
        ["1z|1z|1z|1z"],
        [*("1z" for _ in range(4)), *("2m" for _ in range(10))],
    )
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (_live_angang_action(step=1, seat=0, tile="1z"),),
    )
    browser.screenshot_queue = [_synthetic_blank_screenshot(), screenshot]
    screen = _screen(browser, messages)
    sleep_delays: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    [operation] = state.round.operation_candidates.operations

    result = asyncio.run(screen.operate(operation))

    assert isinstance(result.round.events[-1], AngangEvent)
    assert sleep_delays == [0.2, 1.5]


@pytest.mark.parametrize(
    ("selected_index", "selected_tile", "expected_left"),
    [(0, "4p", 601), (1, "1m", 961)],
)
def test_operate_selects_requested_angang_from_two_candidates(
    monkeypatch: pytest.MonkeyPatch,
    selected_index: int,
    selected_tile: str,
    expected_left: int,
) -> None:
    messages = _angang_messages(
        ["4p|4p|4p|4p", "1m|1m|1m|1m"],
        [
            *("4p" for _ in range(4)),
            *("1m" for _ in range(4)),
            *("2z" for _ in range(6)),
        ],
    )
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (
            _live_angang_action(
                step=1,
                seat=0,
                tile=selected_tile,
            ),
        ),
    )
    screen = _screen(browser, messages)
    sleep_delays: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operations = tuple(
        operation
        for operation in candidates.operations
        if isinstance(operation, AngangOperation)
    )

    state = asyncio.run(screen.operate(operations[selected_index]))

    assert isinstance(state.round.events[-1], AngangEvent)
    assert sleep_delays == [0.4, 1.5]
    assert len(browser.clicked_points) == 2
    button_x, button_y = browser.clicked_points[0]
    assert 900 < button_x < 1050
    assert 650 < button_y < 688
    candidate_x, candidate_y = browser.clicked_points[1]
    assert expected_left < candidate_x < expected_left + 317
    assert 692 < candidate_y < 809


def test_operate_stops_after_showing_three_angang_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _angang_messages(
        [
            "4p|4p|4p|4p",
            "0p|5p|5p|5p",
            "1m|1m|1m|1m",
        ],
        [
            *("4p" for _ in range(4)),
            "0p",
            *("5p" for _ in range(3)),
            *("1m" for _ in range(4)),
            *("2z" for _ in range(2)),
        ],
    )
    screenshot = _gang_button_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = _screen(browser, messages)
    sleep_delays: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    candidates = state.round.operation_candidates
    assert candidates is not None
    operation = candidates.operations[0]

    with pytest.raises(ScreenNotImplementedOperationError) as exc_info:
        asyncio.run(screen.operate(operation))

    assert exc_info.value.screenshot == screenshot
    assert "three angang candidates" in str(exc_info.value)
    assert sleep_delays == [0.4]
    assert len(browser.clicked_points) == 1


def test_operate_accepts_redless_black_five_angang(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _angang_messages(
        ["5s|5s|5s|5s"],
        [*("5s" for _ in range(4)), *("2m" for _ in range(10))],
    )
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (_live_angang_action(step=1, seat=0, tile="5s"),),
    )
    screen = _screen(browser, messages)

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    candidates = state.round.operation_candidates
    assert candidates is not None
    [operation] = candidates.operations

    result = asyncio.run(screen.operate(operation))

    assert isinstance(result.round.events[-1], AngangEvent)


def test_operate_rejects_angang_event_for_different_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _angang_messages(
        ["4p|4p|4p|4p", "1m|1m|1m|1m"],
        [
            *("4p" for _ in range(4)),
            *("1m" for _ in range(4)),
            *("2z" for _ in range(6)),
        ],
    )
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (_live_angang_action(step=1, seat=0, tile="1m"),),
    )
    screen = _screen(browser, messages)

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    candidates = state.round.operation_candidates
    assert candidates is not None
    operation = candidates.operations[0]

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.operate(operation))

    assert exc_info.value.screenshot == screenshot


def test_operate_puts_back_progress_while_waiting_for_gang_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _PutBackTrackingQueue()
    for message in _angang_message_sequence(
        ["1z|1z|1z|1z"],
        [*("1z" for _ in range(4)), *("2m" for _ in range(10))],
    ):
        messages.enqueue(message)
    screenshot = _synthetic_blank_screenshot()
    browser = _MessageOnScreenshotBrowser(
        screenshot,
        messages,
        _live_angang_action(step=1, seat=0, tile="1z"),
    )
    screen = _screen(browser, messages)

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    [operation] = state.round.operation_candidates.operations

    result = asyncio.run(screen.operate(operation))

    assert isinstance(result.round.events[-1], AngangEvent)
    assert messages.put_back_count == 1
    assert browser.clicked_points == []


def test_operate_puts_back_progress_before_selecting_angang_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _PutBackTrackingQueue()
    for message in _angang_message_sequence(
        ["4p|4p|4p|4p", "1m|1m|1m|1m"],
        [
            *("4p" for _ in range(4)),
            *("1m" for _ in range(4)),
            *("2z" for _ in range(6)),
        ],
    ):
        messages.enqueue(message)
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (_live_angang_action(step=1, seat=0, tile="4p"),),
    )
    screen = _screen(browser, messages)

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    candidates = state.round.operation_candidates
    assert candidates is not None
    operation = candidates.operations[0]

    result = asyncio.run(screen.operate(operation))

    assert isinstance(result.round.events[-1], AngangEvent)
    assert messages.put_back_count == 1
    assert len(browser.clicked_points) == 1


def test_operate_does_not_succeed_without_gang_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _angang_messages(
        ["1z|1z|1z|1z"],
        [*("1z" for _ in range(4)), *("2m" for _ in range(10))],
    )
    browser = BrowserControllerSpy(_synthetic_blank_screenshot())
    screen = _screen(browser, messages)
    monkeypatch.setattr(
        match_screen_module,
        "OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS",
        0.001,
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    [operation] = state.round.operation_candidates.operations

    async def operate_with_timeout() -> None:
        async with asyncio.timeout(0.05):
            await screen.operate(operation)

    with pytest.raises(TimeoutError):
        asyncio.run(operate_with_timeout())
    assert browser.clicked_points == []
