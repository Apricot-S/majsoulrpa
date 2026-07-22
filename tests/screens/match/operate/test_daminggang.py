import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import GANG_TEMPLATE_PATH
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import (
    DaminggangEvent,
    DaminggangOperation,
    MatchScreen,
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
    _live_daminggang_action,
    _live_discard_action,
    _live_new_round_action,
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


def _daminggang_messages(
    *combinations: str,
) -> SnifferMessageQueue:
    return _message_queue(
        _auth_game(),
        _live_new_round_action(
            step=0,
            ju=2,
            tiles=["0m", "5m", "5m", "5m", *(["1p"] * 9)],
        ),
        _live_discard_action(
            step=1,
            seat=2,
            tile="5m",
            moqie=False,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=5,
                        combination=list(combinations),
                    )
                ]
            ),
        ),
    )


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


def test_operate_selects_daminggang(monkeypatch: pytest.MonkeyPatch) -> None:
    messages = _daminggang_messages("0m|5m|5m")
    screenshot = _synthetic_template_at_screenshot(
        template_path=GANG_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_daminggang_action(
            step=2,
            seat=0,
            tiles=["0m", "5m", "5m", "5m"],
            froms=[0, 0, 0, 2],
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
    [operation] = candidates.operations
    assert isinstance(operation, DaminggangOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    event = state.round.events[-1]
    assert isinstance(event, DaminggangEvent)
    assert event.from_seat == operation.from_seat
    assert event.tile == operation.tile
    assert event.consumed == operation.consumed
    assert sleep_delays == [1.5]
    [(x, y)] = browser.clicked_points
    assert 900 < x < 1050
    assert 650 < y < 688


def test_operate_retries_until_gang_button_is_drawn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _daminggang_messages("0m|5m|5m")
    button_screenshot = _synthetic_template_at_screenshot(
        template_path=GANG_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        button_screenshot,
        messages,
        _live_daminggang_action(
            step=2,
            seat=0,
            tiles=["0m", "5m", "5m", "5m"],
            froms=[0, 0, 0, 2],
        ),
    )
    browser.screenshot_queue = [
        _synthetic_blank_screenshot(),
        button_screenshot,
    ]
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

    assert isinstance(result.round.events[-1], DaminggangEvent)
    assert sleep_delays == [0.5, 1.5]


def test_operate_rejects_daminggang_event_for_different_combination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _daminggang_messages("0m|5m|5m")
    screenshot = _synthetic_template_at_screenshot(
        template_path=GANG_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_daminggang_action(
            step=2,
            seat=0,
            tiles=["5m", "5m", "5m", "5m"],
            froms=[0, 0, 0, 2],
        ),
    )
    screen = _screen(browser, messages)

    async def skip_sleep(_delay: float) -> None:
        pass

    monkeypatch.setattr(asyncio, "sleep", skip_sleep)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    [operation] = state.round.operation_candidates.operations

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.operate(operation))

    assert exc_info.value.screenshot == screenshot


def test_operate_rejects_multiple_daminggang_candidates() -> None:
    messages = _daminggang_messages("0m|5m|5m", "5m|5m|5m")
    screenshot = _synthetic_template_at_screenshot(
        template_path=GANG_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = BrowserControllerSpy(screenshot)
    screen = _screen(browser, messages)

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())
    assert state.round.operation_candidates is not None
    operation = state.round.operation_candidates.operations[0]

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.operate(operation))

    assert exc_info.value.screenshot == screenshot
    assert browser.clicked_points == []


def test_operate_puts_back_progress_while_waiting_for_gang_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _PutBackTrackingQueue()
    for message in (
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
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=5,
                        combination=["0m|5m|5m"],
                    )
                ]
            ),
        ),
    ):
        messages.enqueue(message)
    browser = _MessageOnScreenshotBrowser(
        _synthetic_blank_screenshot(),
        messages,
        _live_daminggang_action(
            step=2,
            seat=0,
            tiles=["0m", "5m", "5m", "5m"],
            froms=[0, 0, 0, 2],
        ),
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

    assert isinstance(result.round.events[-1], DaminggangEvent)
    assert messages.put_back_count == 1
    assert browser.clicked_points == []


def test_operate_does_not_succeed_without_gang_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _daminggang_messages("0m|5m|5m")
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
