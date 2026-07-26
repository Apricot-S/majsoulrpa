import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.assets.templates.match import (
    SKIP_SETTINGS_PATH,
    SKIP_TEMPLATE_PATH,
)
from majsoulrpa.screens.match import (
    MatchScreen,
    PengEvent,
    SkipOperation,
    ZimoEvent,
)
from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
    _request_response,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
    _live_peng_action,
)


class _MessageOnFirstClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        message: DecodedSnifferMessage,
        *screenshots: bytes,
    ) -> None:
        super().__init__(screenshot, *screenshots)
        self._messages = messages
        self._message = message
        self.click_warps: list[bool] = []

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        self.click_warps.append(warp)
        await super().click(x, y, warp=warp)
        if len(self.clicked_points) == 1:
            self._messages.enqueue(self._message)


class _FailToDisableNoCallBrowser(_MessageOnFirstClickBrowser):
    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        if self.clicked_points:
            msg = "cannot disable no-call"
            raise RuntimeError(msg)
        await super().click(x, y, warp=warp)


class _MessageOnEachClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        *click_messages: DecodedSnifferMessage,
    ) -> None:
        super().__init__(screenshot)
        self._messages = messages
        self._click_messages = iter(click_messages)
        self.click_warps: list[bool] = []

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        self.click_warps.append(warp)
        await super().click(x, y, warp=warp)
        try:
            message = next(self._click_messages)
        except StopIteration:
            return
        self._messages.enqueue(message)


@pytest.mark.parametrize(
    ("player_count", "scores", "toggle_top"),
    [
        (4, [25000] * 4, 655),
        (3, [35000] * 3, 623),
    ],
)
def test_operate_skip_toggles_no_call_until_next_action(
    player_count: int,
    scores: list[int],
    toggle_top: int,
) -> None:
    discard_seat = player_count - 1
    messages = _message_queue(
        _auth_game(player_count=player_count),
        _live_new_round_action(
            step=0,
            ju=discard_seat,
            scores=scores,
            tiles=["5m", "5m", *["1p"] * 11],
        ),
        _live_discard_action(
            step=1,
            seat=discard_seat,
            tile="5m",
            moqie=False,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=3,
                        combination=["5m|5m"],
                    ),
                ],
            ),
        ),
    )
    browser = _MessageOnFirstClickBrowser(
        b"synthetic-screenshot",
        messages,
        _live_deal_action(
            step=2,
            seat=0,
            tile="9s",
            left_tile_count=68,
        ),
    )
    screen = _screen(browser, messages)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None
    operation = candidates.operations[-1]
    assert operation == SkipOperation()

    state = asyncio.run(screen.operate(operation))

    assert isinstance(state.round.events[-1], ZimoEvent)
    assert browser.click_warps == [True, True]
    assert len(browser.clicked_points) == 2
    for x, y in browser.clicked_points:
        assert 18 < x < 60
        assert toggle_top < y < toggle_top + 42


def test_no_call_toggle_accepts_input_chi_peng_gang_response() -> None:
    messages = _message_queue(
        _auth_game(player_count=4),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=["5m", "5m", *["1p"] * 11],
        ),
        _live_discard_action(
            step=1,
            seat=3,
            tile="5m",
            moqie=False,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=3,
                        combination=["5m|5m"],
                    ),
                ],
            ),
        ),
    )
    browser = _MessageOnEachClickBrowser(
        b"synthetic-screenshot",
        messages,
        _request_response(".lq.FastTest.inputChiPengGang", response={}),
        _live_deal_action(
            step=2,
            seat=0,
            tile="9s",
            left_tile_count=68,
        ),
    )
    screen = _screen(browser, messages)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None

    state = asyncio.run(
        asyncio.wait_for(
            screen.operate(candidates.operations[-1]),
            timeout=1.0,
        )
    )

    assert isinstance(state.round.events[-1], ZimoEvent)
    assert browser.click_warps == [True, True]


def test_operate_skip_detects_skip_button_at_short_interval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = _message_queue(
        _auth_game(player_count=4),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=["1m"] * 13,
        ),
        _live_discard_action(
            step=1,
            seat=3,
            tile="9s",
            moqie=False,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(type=9, combination=[]),
                ],
            ),
        ),
    )
    browser = _MessageOnFirstClickBrowser(
        _synthetic_blank_screenshot(),
        messages,
        _live_deal_action(
            step=2,
            seat=0,
            tile="9s",
            left_tile_count=68,
        ),
        _synthetic_template_screenshot(
            template_path=SKIP_TEMPLATE_PATH,
            settings_path=SKIP_SETTINGS_PATH,
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
    operation = candidates.operations[-1]
    assert operation == SkipOperation()

    state = asyncio.run(screen.operate(operation))

    assert isinstance(state.round.events[-1], ZimoEvent)
    assert sleep_delays == [0.2]
    assert browser.click_warps == [True]
    assert len(browser.clicked_points) == 1


def test_operate_skip_restores_no_call_after_preemption() -> None:
    messages = _message_queue(
        _auth_game(player_count=4),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=["3m", "4m", *["1p"] * 11],
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
                    ),
                ],
            ),
        ),
    )
    browser = _MessageOnFirstClickBrowser(
        b"synthetic-screenshot",
        messages,
        _live_peng_action(
            step=2,
            seat=1,
            tiles=["5m", "5m", "5m"],
            froms=[1, 1, 3],
        ),
    )
    screen = _screen(browser, messages)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None

    state = asyncio.run(screen.operate(candidates.operations[-1]))

    assert isinstance(state.round.events[-1], PengEvent)
    assert browser.click_warps == [True, True]
    assert len(browser.clicked_points) == 2


def test_operate_skip_does_not_hide_no_call_cleanup_failure() -> None:
    messages = _message_queue(
        _auth_game(player_count=4),
        _live_new_round_action(
            step=0,
            ju=3,
            tiles=["5m", "5m", *["1p"] * 11],
        ),
        _live_discard_action(
            step=1,
            seat=3,
            tile="5m",
            moqie=False,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(
                        type=3,
                        combination=["5m|5m"],
                    ),
                ],
            ),
        ),
    )
    browser = _FailToDisableNoCallBrowser(
        b"synthetic-screenshot",
        messages,
        _live_deal_action(
            step=2,
            seat=0,
            tile="9s",
            left_tile_count=68,
        ),
    )
    screen = _screen(browser, messages)

    asyncio.run(screen.before_callback())
    initial = asyncio.run(screen.get_state())
    candidates = initial.round.operation_candidates
    assert candidates is not None

    with pytest.raises(RuntimeError, match="cannot disable no-call"):
        asyncio.run(screen.operate(candidates.operations[-1]))


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
