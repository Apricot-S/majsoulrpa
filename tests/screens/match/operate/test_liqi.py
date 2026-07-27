import asyncio
from random import Random
from types import SimpleNamespace

import pytest

import majsoulrpa.screens.match.screen as match_screen_module
from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import LIQI_TEMPLATE_PATH
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import (
    DapaiEvent,
    LiqiOperation,
    MatchScreen,
    validate_tile,
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
    _live_deal_action,
    _live_discard_action,
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


def _liqi_messages(candidate: str) -> SnifferMessageQueue:
    return _message_queue(
        _auth_game(),
        _live_new_round_action(step=0, ju=1),
        _live_discard_action(step=1, seat=3, tile="9p", moqie=False),
        _live_deal_action(
            step=2,
            seat=0,
            tile="9s",
            left_tile_count=68,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=7,
                        combination=[candidate],
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


def _get_liqi_operation(
    screen: MatchScreen,
    *,
    tile: str,
    moqie: bool,
) -> LiqiOperation:
    state = asyncio.run(screen.get_state())
    candidates = state.round.operation_candidates
    assert candidates is not None
    return next(
        operation
        for operation in candidates.operations
        if isinstance(operation, LiqiOperation)
        and operation.tile == validate_tile(tile)
        and operation.moqie is moqie
    )


@pytest.mark.parametrize(
    ("tile", "moqie", "liqi", "wliqi", "expected_left"),
    [
        ("1m", False, True, False, 232),
        ("9s", True, False, True, 1495),
    ],
)
def test_operate_selects_liqi_discard(
    monkeypatch: pytest.MonkeyPatch,
    *,
    tile: str,
    moqie: bool,
    liqi: bool,
    wliqi: bool,
    expected_left: int,
) -> None:
    messages = _liqi_messages(tile)
    screenshot = _synthetic_template_at_screenshot(
        template_path=LIQI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (
            _live_discard_action(
                step=3,
                seat=0,
                tile=tile,
                moqie=moqie,
                liqi=liqi,
                wliqi=wliqi,
            ),
        ),
    )
    screen = _screen(browser, messages)
    sleep_delays: list[float] = []

    async def record_sleep(delay: float) -> None:
        sleep_delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    asyncio.run(screen.before_callback())
    operation = _get_liqi_operation(screen, tile=tile, moqie=moqie)
    state = asyncio.run(screen.operate(operation))

    assert state.round.events[-1] == DapaiEvent(
        action_step=3,
        seat=state.self_seat,
        tile=validate_tile(tile),
        moqie=moqie,
        liqi=liqi,
        wliqi=wliqi,
        dora_indicators=(),
    )
    assert sleep_delays == [0.4]
    assert len(browser.clicked_points) == 2
    button_x, button_y = browser.clicked_points[0]
    assert 900 < button_x < 1050
    assert 650 < button_y < 688
    tile_x, tile_y = browser.clicked_points[1]
    assert expected_left < tile_x < expected_left + 71
    assert 936 < tile_y < 1040


def test_operate_retries_liqi_button_detection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _liqi_messages("9s")
    button_screenshot = _synthetic_template_at_screenshot(
        template_path=LIQI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesByClickBrowser(
        _synthetic_blank_screenshot(),
        messages,
        (),
        (
            _live_discard_action(
                step=3,
                seat=0,
                tile="9s",
                moqie=True,
                liqi=True,
            ),
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
    operation = _get_liqi_operation(screen, tile="9s", moqie=True)
    asyncio.run(screen.operate(operation))

    assert sleep_delays == [0.2, 0.4]
    assert len(browser.clicked_points) == 2


def test_operate_does_not_click_liqi_tile_after_action_arrives(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _liqi_messages("9s")
    screenshot = _synthetic_template_at_screenshot(
        template_path=LIQI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (
            _live_discard_action(
                step=3,
                seat=0,
                tile="9s",
                moqie=True,
                liqi=True,
            ),
        ),
    )
    screen = _screen(browser, messages)

    async def complete_sleep_immediately(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", complete_sleep_immediately)

    asyncio.run(screen.before_callback())
    operation = _get_liqi_operation(screen, tile="9s", moqie=True)
    state = asyncio.run(screen.operate(operation))

    event = state.round.events[-1]
    assert isinstance(event, DapaiEvent)
    assert event.liqi is True
    assert len(browser.clicked_points) == 1


@pytest.mark.parametrize(
    ("actual_tile", "actual_moqie", "actual_liqi"),
    [
        ("1m", False, True),
        ("9s", False, True),
        ("9s", True, False),
    ],
)
def test_operate_rejects_mismatched_liqi_discard(
    monkeypatch: pytest.MonkeyPatch,
    *,
    actual_tile: str,
    actual_moqie: bool,
    actual_liqi: bool,
) -> None:
    messages = _liqi_messages("9s")
    screenshot = _synthetic_template_at_screenshot(
        template_path=LIQI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (
            _live_discard_action(
                step=3,
                seat=0,
                tile=actual_tile,
                moqie=actual_moqie,
                liqi=actual_liqi,
            ),
        ),
    )
    screen = _screen(browser, messages)

    async def complete_sleep_immediately(delay: float) -> None:
        _ = delay

    monkeypatch.setattr(asyncio, "sleep", complete_sleep_immediately)

    asyncio.run(screen.before_callback())
    operation = _get_liqi_operation(screen, tile="9s", moqie=True)
    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.operate(operation))


def test_operate_does_not_succeed_without_liqi_button(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _liqi_messages("9s")
    browser = _MessagesByClickBrowser(
        _synthetic_blank_screenshot(),
        messages,
    )
    screen = _screen(browser, messages)
    monkeypatch.setattr(
        match_screen_module,
        "OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS",
        0.001,
    )

    asyncio.run(screen.before_callback())
    operation = _get_liqi_operation(screen, tile="9s", moqie=True)

    async def operate_with_timeout() -> None:
        async with asyncio.timeout(0.05):
            await screen.operate(operation)

    with pytest.raises(TimeoutError):
        asyncio.run(operate_with_timeout())
    assert browser.clicked_points == []


def test_operate_retries_liqi_tile_click_until_input_progress(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _liqi_messages("9s")
    screenshot = _synthetic_template_at_screenshot(
        template_path=LIQI_TEMPLATE_PATH,
        left=900,
        top=650,
    )
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (),
        (
            _live_discard_action(
                step=3,
                seat=0,
                tile="9s",
                moqie=True,
                liqi=True,
            ),
        ),
    )
    screen = _screen(browser, messages)
    monkeypatch.setattr(
        match_screen_module,
        "DAPAI_CLICK_RETRY_INTERVAL_SECONDS",
        0.001,
    )
    original_sleep = asyncio.sleep

    async def skip_option_display_delay(delay: float) -> None:
        if delay == 0.4:
            return
        await original_sleep(delay)

    monkeypatch.setattr(asyncio, "sleep", skip_option_display_delay)

    asyncio.run(screen.before_callback())
    operation = _get_liqi_operation(screen, tile="9s", moqie=True)
    asyncio.run(screen.operate(operation))

    assert len(browser.clicked_points) == 3
