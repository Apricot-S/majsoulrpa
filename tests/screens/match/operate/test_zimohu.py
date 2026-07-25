import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match import HuleEvent, MatchScreen, ZimohuOperation
from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
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
    _live_hule_action,
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
        for message in self._messages_on_click:
            self._messages.enqueue(message)


@pytest.mark.parametrize(
    ("player_count", "old_scores", "delta_scores", "scores", "region_top"),
    [
        (
            4,
            [25000] * 4,
            [3000, -1000, -1000, -1000],
            [28000, 24000, 24000, 24000],
            590,
        ),
        (3, [35000] * 3, [2000, -1000, -1000], [37000, 34000, 34000], 558),
    ],
)
def test_operate_enables_auto_hule_and_waits_for_zimohu(
    monkeypatch: pytest.MonkeyPatch,
    player_count: int,
    old_scores: list[int],
    delta_scores: list[int],
    scores: list[int],
    region_top: int,
) -> None:
    messages = _message_queue(
        _auth_game(player_count=player_count),
        _live_new_round_action(step=0, ju=1, scores=old_scores),
        _live_discard_action(
            step=1,
            seat=2,
            tile="9s",
            moqie=False,
        ),
        _live_deal_action(
            step=2,
            seat=0,
            tile="5p",
            left_tile_count=68,
            operation=liqi_pb2.OptionalOperationList(
                operation_list=[
                    liqi_pb2.OptionalOperation(type=8, combination=[]),
                ],
            ),
        ),
    )
    browser = _MessagesOnClickBrowser(
        b"synthetic-screenshot",
        messages,
        _live_hule_action(
            step=3,
            hules=[
                liqi_pb2.HuleInfo(
                    hand=["1m"] * 13,
                    hu_tile="5p",
                    seat=0,
                    zimo=True,
                    fu=30,
                ),
            ],
            old_scores=old_scores,
            delta_scores=delta_scores,
            scores=scores,
            doras=[],
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
    [operation] = candidates.operations
    assert isinstance(operation, ZimohuOperation)

    state = asyncio.run(screen.operate(operation))

    assert state.version == initial.version + 1
    event = state.round.events[-1]
    assert isinstance(event, HuleEvent)
    assert event.hules[0].hu_tile == operation.tile
    assert sleep_delays == []
    assert browser.click_warps == [True]
    [(x, y)] = browser.clicked_points
    assert 18 < x < 60
    assert region_top < y < region_top + 42
