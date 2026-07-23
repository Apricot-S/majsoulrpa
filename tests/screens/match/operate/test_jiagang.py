import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import GANG_TEMPLATE_PATH
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
    ScreenNotImplementedOperationError,
)
from majsoulrpa.screens.match import (
    JiagangEvent,
    JiagangOperation,
    MatchScreen,
)
from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _synthetic_template_at_screenshot,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_deal_action,
    _live_discard_action,
    _live_jiagang_action,
    _live_new_round_action,
    _live_peng_action,
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


def _jiagang_message_sequence(
    combinations: list[str],
) -> tuple[
    tuple[DecodedSnifferMessage, ...],
    tuple[str, ...],
    int,
]:
    peng_tiles_by_combination = {
        "4p|4p|4p|4p": ("4p", ("4p", "4p"), "4p"),
        "0p|5p|5p|5p": ("5p", ("5p", "5p"), "0p"),
        "1m|1m|1m|1m": ("1m", ("1m", "1m"), "1m"),
        "0m|5m|5m|5m": ("5m", ("0m", "5m"), "5m"),
    }
    pengs = tuple(
        peng_tiles_by_combination[combination] for combination in combinations
    )
    fillers = ("2z",) * (13 - 3 * len(pengs))
    tiles = [
        tile
        for _claimed, consumed, added in pengs
        for tile in (*consumed, added)
    ]
    tiles.extend(fillers)

    messages: list[DecodedSnifferMessage] = [
        _auth_game(),
        _live_new_round_action(step=0, ju=2, tiles=tiles),
    ]
    step = 1
    for claimed, consumed, _added in pengs:
        messages.extend(
            (
                _live_discard_action(
                    step=step,
                    seat=2,
                    tile=claimed,
                    moqie=False,
                ),
                _live_peng_action(
                    step=step + 1,
                    seat=0,
                    tiles=[*consumed, claimed],
                    froms=[0, 0, 2],
                ),
                _live_discard_action(
                    step=step + 2,
                    seat=0,
                    tile="2z",
                    moqie=False,
                ),
                _live_deal_action(
                    step=step + 3,
                    seat=2,
                    tile="",
                    left_tile_count=69 - step,
                ),
            )
        )
        step += 4

    messages.extend(
        (
            _live_discard_action(
                step=step,
                seat=2,
                tile="9s",
                moqie=True,
            ),
            _live_deal_action(
                step=step + 1,
                seat=0,
                tile="3z",
                left_tile_count=69 - step,
                operation=liqi_pb2.OptionalOperationList(
                    operation_list=[
                        liqi_pb2.OptionalOperation(
                            type=6,
                            combination=combinations,
                        )
                    ]
                ),
            ),
        )
    )
    return (
        tuple(messages),
        tuple(added for _, _, added in pengs),
        step + 2,
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


def _message_queue(
    *messages: DecodedSnifferMessage,
) -> SnifferMessageQueue:
    queue = SnifferMessageQueue(
        capacity=len(messages) + 2,
        max_payload_bytes=4096,
    )
    for message in messages:
        queue.enqueue(message)
    return queue


def _gang_button_screenshot() -> bytes:
    return _synthetic_template_at_screenshot(
        template_path=GANG_TEMPLATE_PATH,
        left=900,
        top=650,
    )


def test_operate_selects_only_jiagang_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sequence, (added,), next_step = _jiagang_message_sequence(["0m|5m|5m|5m"])
    messages = _message_queue(*sequence)
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (
            _live_jiagang_action(
                step=next_step,
                seat=0,
                added=added,
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
    [operation] = candidates.operations
    assert isinstance(operation, JiagangOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    event = state.round.events[-1]
    assert isinstance(event, JiagangEvent)
    assert event.added == operation.added
    assert sleep_delays == [1.5]
    assert len(browser.clicked_points) == 1


@pytest.mark.parametrize(
    ("selected_index", "expected_left"),
    [(0, 601), (1, 961)],
)
def test_operate_selects_requested_jiagang_from_two_candidates(
    monkeypatch: pytest.MonkeyPatch,
    selected_index: int,
    expected_left: int,
) -> None:
    sequence, added_tiles, next_step = _jiagang_message_sequence(
        ["4p|4p|4p|4p", "1m|1m|1m|1m"]
    )
    messages = _message_queue(*sequence)
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (
            _live_jiagang_action(
                step=next_step,
                seat=0,
                added=added_tiles[selected_index],
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
        if isinstance(operation, JiagangOperation)
    )

    state = asyncio.run(screen.operate(operations[selected_index]))

    event = state.round.events[-1]
    assert isinstance(event, JiagangEvent)
    assert event.added == operations[selected_index].added
    assert sleep_delays == [0.4, 1.5]
    assert len(browser.clicked_points) == 2
    candidate_x, candidate_y = browser.clicked_points[1]
    assert expected_left < candidate_x < expected_left + 317
    assert 692 < candidate_y < 809


def test_operate_stops_after_showing_three_jiagang_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sequence, _added_tiles, _next_step = _jiagang_message_sequence(
        [
            "4p|4p|4p|4p",
            "0p|5p|5p|5p",
            "1m|1m|1m|1m",
        ]
    )
    messages = _message_queue(*sequence)
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
    assert "three jiagang candidates" in str(exc_info.value)
    assert sleep_delays == [0.4]
    assert len(browser.clicked_points) == 1


def test_operate_rejects_jiagang_event_for_different_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sequence, added_tiles, next_step = _jiagang_message_sequence(
        ["4p|4p|4p|4p", "1m|1m|1m|1m"]
    )
    messages = _message_queue(*sequence)
    screenshot = _gang_button_screenshot()
    browser = _MessagesByClickBrowser(
        screenshot,
        messages,
        (),
        (
            _live_jiagang_action(
                step=next_step,
                seat=0,
                added=added_tiles[1],
            ),
        ),
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
