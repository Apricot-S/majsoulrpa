import asyncio
from random import Random
from types import SimpleNamespace

import pytest

from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match import (
    Babei,
    BabeiEvent,
    MatchScreen,
    ZimoEvent,
)
from majsoulrpa.sniffer.events import DecodedSnifferMessage
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import (
    SELF_ACCOUNT_ID,
    _auth_game,
    _live_babei_action,
    _live_deal_action,
    _live_discard_action,
    _live_new_round_action,
)


def _screen(
    *messages: DecodedSnifferMessage,
    screenshot: bytes = b"synthetic-screenshot",
) -> MatchScreen:
    return MatchScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            rng=Random(0),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
            sniffer_messages=_message_queue(*messages),
        ),
    )


def test_get_state_applies_self_moqie_babei() -> None:
    screen = _screen(
        _auth_game(player_count=3),
        _live_new_round_action(step=0, ju=1, scores=[35000] * 3),
        _live_discard_action(step=1, seat=1, tile="1s", moqie=False),
        _live_deal_action(
            step=2,
            seat=0,
            tile="4z",
            left_tile_count=54,
        ),
        _live_babei_action(
            step=3,
            seat=0,
            moqie=True,
            doras=["3p", "4p"],
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("1m",) * 13
    assert state.round.zimopai is None
    assert state.round.babei[0] == (Babei(moqie=True),)
    assert state.round.fulu[0] == ()
    assert state.round.he[0] == ()
    assert state.round.dora_indicators == ("3p", "4p")
    assert state.round.pending_action_target == (0, "4z")
    assert state.round.first_draw == (False,) * 3
    assert state.round.yifa == (False,) * 3
    assert state.round.lingshang_zimo == (True, False, False)
    assert isinstance(state.round.events[-1], BabeiEvent)


def test_get_state_applies_self_hand_babei() -> None:
    screen = _screen(
        _auth_game(player_count=3),
        _live_new_round_action(
            step=0,
            ju=1,
            scores=[35000] * 3,
            tiles=["4z", *(["1m"] * 12)],
        ),
        _live_discard_action(step=1, seat=1, tile="1s", moqie=False),
        _live_deal_action(
            step=2,
            seat=0,
            tile="2p",
            left_tile_count=54,
        ),
        _live_babei_action(step=3, seat=0, moqie=False),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == (*(("1m",) * 12), "2p")
    assert state.round.zimopai is None
    assert state.round.babei[0] == (Babei(moqie=False),)
    assert state.round.pending_action_target == (0, "4z")


def test_get_state_applies_lingshang_zimo_after_babei() -> None:
    screen = _screen(
        _auth_game(player_count=3),
        _live_new_round_action(step=0, ju=1, scores=[35000] * 3),
        _live_discard_action(step=1, seat=1, tile="1s", moqie=False),
        _live_deal_action(
            step=2,
            seat=0,
            tile="4z",
            left_tile_count=54,
        ),
        _live_babei_action(step=3, seat=0, moqie=True),
        _live_deal_action(
            step=4,
            seat=0,
            tile="2p",
            left_tile_count=53,
        ),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert isinstance(state.round.events[-1], ZimoEvent)
    assert state.round.zimopai == "2p"
    assert state.round.pending_action_target is None
    assert state.round.lingshang_zimo == (True, False, False)


def test_get_state_applies_opponent_babei() -> None:
    screen = _screen(
        _auth_game(player_count=3),
        _live_new_round_action(step=0, ju=1, scores=[35000] * 3),
        _live_babei_action(step=1, seat=1, moqie=True),
    )

    asyncio.run(screen.before_callback())
    state = asyncio.run(screen.get_state())

    assert state.round.shoupai == ("1m",) * 13
    assert state.round.babei[1] == (Babei(moqie=True),)
    assert state.round.pending_action_target == (1, "4z")
    assert state.round.lingshang_zimo == (False, True, False)


def test_get_state_rejects_babei_in_four_player_match() -> None:
    screen = _screen(
        _auth_game(),
        _live_new_round_action(step=0, ju=1),
        _live_babei_action(step=1, seat=1, moqie=True),
        screenshot=b"inconsistent-screenshot",
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"


@pytest.mark.parametrize(
    ("tiles", "drawn_tile", "moqie"),
    [
        (["4z", *(["1m"] * 12)], "2p", True),
        (["1m"] * 13, "2p", False),
    ],
)
def test_get_state_rejects_self_babei_inconsistent_with_moqie(
    tiles: list[str],
    drawn_tile: str,
    *,
    moqie: bool,
) -> None:
    screen = _screen(
        _auth_game(player_count=3),
        _live_new_round_action(
            step=0,
            ju=1,
            scores=[35000] * 3,
            tiles=tiles,
        ),
        _live_discard_action(step=1, seat=1, tile="1s", moqie=False),
        _live_deal_action(
            step=2,
            seat=0,
            tile=drawn_tile,
            left_tile_count=54,
        ),
        _live_babei_action(step=3, seat=0, moqie=moqie),
        screenshot=b"inconsistent-screenshot",
    )

    asyncio.run(screen.before_callback())
    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == b"inconsistent-screenshot"
