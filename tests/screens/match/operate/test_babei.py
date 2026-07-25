import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import BABEI_TEMPLATE_PATH
from majsoulrpa.screens.match import BabeiEvent, BabeiOperation, MatchScreen
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
    _live_babei_action,
    _live_deal_action,
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
        super().__init__(capacity=10, max_payload_bytes=4096)
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


def _babei_messages() -> SnifferMessageQueue:
    return _message_queue(
        _auth_game(player_count=3),
        _live_new_round_action(
            step=0,
            ju=0,
            scores=[35000] * 3,
            tiles=[*(["1m"] * 12), "4z", "4z"],
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(type=11, combination=[])
                ]
            ),
        ),
    )


def _hand_babei_messages() -> SnifferMessageQueue:
    return _message_queue(
        _auth_game(player_count=3),
        _live_new_round_action(
            step=0,
            ju=1,
            scores=[35000] * 3,
            tiles=["4z", *(["1m"] * 12)],
        ),
        _live_discard_action(
            step=1,
            seat=1,
            tile="1s",
            moqie=False,
        ),
        _live_deal_action(
            step=2,
            seat=0,
            tile="2p",
            left_tile_count=54,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(type=11, combination=[])
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


def test_operate_selects_drawn_north_before_hand_north(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _babei_messages()
    screenshot = _synthetic_template_at_screenshot(
        template_path=BABEI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_babei_action(step=1, seat=0, moqie=True),
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
    assert isinstance(operation, BabeiOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    event = state.round.events[-1]
    assert isinstance(event, BabeiEvent)
    assert event.moqie
    assert sleep_delays == [1.5]
    [(x, y)] = browser.clicked_points
    assert 900 < x < 1050
    assert 650 < y < 688


def test_operate_retries_until_babei_button_is_drawn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _babei_messages()
    button_screenshot = _synthetic_template_at_screenshot(
        template_path=BABEI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        button_screenshot,
        messages,
        _live_babei_action(step=1, seat=0, moqie=True),
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

    assert isinstance(result.round.events[-1], BabeiEvent)
    assert sleep_delays == [0.5, 1.5]


def test_operate_accepts_automatically_selected_hand_babei(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _hand_babei_messages()
    screenshot = _synthetic_template_at_screenshot(
        template_path=BABEI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesOnClickBrowser(
        screenshot,
        messages,
        _live_babei_action(step=3, seat=0, moqie=False),
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

    event = result.round.events[-1]
    assert isinstance(event, BabeiEvent)
    assert not event.moqie


def test_operate_puts_back_progress_while_waiting_for_babei_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _PutBackTrackingQueue()
    initial_messages = _babei_messages()
    while (message := initial_messages.get_nowait()) is not None:
        messages.enqueue(message)
    browser = _MessageOnScreenshotBrowser(
        _synthetic_blank_screenshot(),
        messages,
        _live_babei_action(step=1, seat=0, moqie=True),
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

    assert isinstance(result.round.events[-1], BabeiEvent)
    assert messages.put_back_count == 1
    assert browser.clicked_points == []


def test_operate_does_not_succeed_without_babei_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _babei_messages()
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
