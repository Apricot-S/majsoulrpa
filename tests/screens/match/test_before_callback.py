import asyncio
from random import Random

from majsoulrpa.presentation import Region
from majsoulrpa.screens.match import MatchScreen
from tests.screens._support import BrowserControllerSpy, ScreenContext


def test_match_screen_before_callback_moves_mouse_away_from_hand() -> None:
    assert (
        Region(left=585, top=790, width=1000, height=70)
        == MatchScreen.MOUSE_SAFE_REGION
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = MatchScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )

    asyncio.run(screen.before_callback())

    [(x, y)] = browser.moved_points
    assert 585 < x < 1585
    assert 790 < y < 860
    assert browser.events == ["move_mouse"]
