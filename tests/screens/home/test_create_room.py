import asyncio
import logging
from inspect import signature
from random import Random

import pytest

import majsoulrpa.screens.home as home_module
from majsoulrpa.assets.templates.home import (
    CREATE_ROOM_SETTINGS_PATH,
    CREATE_ROOM_TEMPLATE_PATH,
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.assets.templates.home.create_room import (
    CREATE_SETTINGS_PATH,
    CREATE_TEMPLATE_PATH,
)
from majsoulrpa.presentation import Region
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenStaleError,
)
from majsoulrpa.screens.home import (
    HomeScreen,
    Length,
    Mode,
    ThinkingTime,
)
from tests.screens.home._support import (
    BrowserControllerSpy,
    ScreenContext,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)


def test_room_creation_enums_have_expected_members() -> None:
    assert list(Mode) == [Mode.FOUR_PLAYER, Mode.THREE_PLAYER]
    assert list(Length) == [
        Length.ONE_GAME,
        Length.EAST_ONLY,
        Length.TWO_WIND_MATCH,
        Length.VS_AI,
    ]
    assert list(ThinkingTime) == [
        ThinkingTime.THREE_PLUS_FIVE,
        ThinkingTime.FIVE_PLUS_TEN,
        ThinkingTime.FIVE_PLUS_TWENTY,
        ThinkingTime.SIXTY_PLUS_ZERO,
        ThinkingTime.THREE_HUNDRED_PLUS_ZERO,
    ]


def test_mode_regions_have_placeholder_for_each_mode() -> None:
    assert set(HomeScreen.MODE_REGIONS) == set(Mode)
    assert all(
        isinstance(region, Region)
        for region in HomeScreen.MODE_REGIONS.values()
    )


def test_length_regions_have_placeholder_for_each_length() -> None:
    assert set(HomeScreen.LENGTH_REGIONS) == set(Length)
    assert all(
        isinstance(region, Region)
        for region in HomeScreen.LENGTH_REGIONS.values()
    )


def test_thinking_time_regions_have_placeholder_for_each_thinking_time() -> (
    None
):
    assert set(HomeScreen.THINKING_TIME_REGIONS) == set(ThinkingTime)
    assert all(
        isinstance(region, Region)
        for region in HomeScreen.THINKING_TIME_REGIONS.values()
    )


def test_create_room_defaults_to_four_player_two_wind_five_plus_twenty(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    screen = HomeScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(
                _synthetic_template_screenshot(
                    template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
                    settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
                ),
                _synthetic_template_screenshot(
                    template_path=CREATE_ROOM_TEMPLATE_PATH,
                    settings_path=CREATE_ROOM_SETTINGS_PATH,
                ),
                _synthetic_template_screenshot(
                    template_path=CREATE_TEMPLATE_PATH,
                    settings_path=CREATE_SETTINGS_PATH,
                ),
            ),
        ),
    )
    parameters = signature(HomeScreen.create_room).parameters

    assert parameters["mode"].default is Mode.FOUR_PLAYER
    assert parameters["length"].default is Length.TWO_WIND_MATCH
    assert parameters["thinking_time"].default is ThinkingTime.FIVE_PLUS_TWENTY
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        result = asyncio.run(screen.create_room())

    assert result is None
    assert (
        "screen API called: screen=HomeScreen api=create_room" in caplog.text
    )


def test_create_room_accepts_each_enum_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def sleep(_seconds: float) -> None:
        pass

    def create_screen() -> HomeScreen:
        return HomeScreen(
            context=ScreenContext(
                browser=BrowserControllerSpy(
                    _synthetic_template_screenshot(
                        template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
                        settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
                    ),
                    _synthetic_template_screenshot(
                        template_path=CREATE_ROOM_TEMPLATE_PATH,
                        settings_path=CREATE_ROOM_SETTINGS_PATH,
                    ),
                    _synthetic_template_screenshot(
                        template_path=CREATE_TEMPLATE_PATH,
                        settings_path=CREATE_SETTINGS_PATH,
                    ),
                ),
            ),
        )

    async def create_rooms() -> list[None]:
        results = [
            await create_screen().create_room(mode=mode) for mode in Mode
        ]
        results.extend(
            [
                await create_screen().create_room(length=length)
                for length in Length
            ],
        )
        results.extend(
            [
                await create_screen().create_room(thinking_time=thinking_time)
                for thinking_time in ThinkingTime
            ],
        )
        return results

    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    assert asyncio.run(create_rooms()) == [None] * (
        len(Mode) + len(Length) + len(ThinkingTime)
    )


def test_create_room_clicks_settings_then_create_at_half_second_intervals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    timeline: list[str] = []

    class OrderedBrowserControllerSpy(BrowserControllerSpy):
        async def click(
            self,
            x: float,
            y: float,
            *,
            warp: bool = False,
        ) -> None:
            timeline.append("click")
            await super().click(x, y, warp=warp)

        async def screenshot(self) -> bytes:
            timeline.append("screenshot")
            return await super().screenshot()

    async def sleep(seconds: float) -> None:
        timeline.append(f"sleep:{seconds}")

    browser = OrderedBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_ROOM_TEMPLATE_PATH,
            settings_path=CREATE_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_TEMPLATE_PATH,
            settings_path=CREATE_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(
        context=ScreenContext(browser=browser, rng=Random(0)),
    )
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    result = asyncio.run(screen.create_room())

    assert result is None
    assert screen._stale
    assert len(browser.clicked_points) == 6
    for point, region in zip(
        browser.clicked_points[2:5],
        (
            HomeScreen.MODE_REGIONS[Mode.FOUR_PLAYER],
            HomeScreen.LENGTH_REGIONS[Length.TWO_WIND_MATCH],
            HomeScreen.THINKING_TIME_REGIONS[ThinkingTime.FIVE_PLUS_TWENTY],
        ),
        strict=True,
    ):
        x, y = point
        assert region.left < x < region.right
        assert region.top < y < region.bottom
    assert timeline == [
        "screenshot",
        "click",
        "sleep:1.0",
        "screenshot",
        "click",
        "sleep:1.0",
        "screenshot",
        "click",
        "sleep:0.5",
        "click",
        "sleep:0.5",
        "click",
        "sleep:0.5",
        "click",
    ]


@pytest.mark.parametrize("failing_click_number", [3, 6])
def test_create_room_remains_active_when_setting_or_create_click_fails(
    monkeypatch: pytest.MonkeyPatch,
    failing_click_number: int,
) -> None:
    class FailingBrowserControllerSpy(BrowserControllerSpy):
        def __init__(self, screenshot: bytes, *screenshots: bytes) -> None:
            super().__init__(screenshot, *screenshots)
            self.click_count = 0

        async def click(
            self,
            x: float,
            y: float,
            *,
            warp: bool = False,
        ) -> None:
            self.click_count += 1
            if self.click_count == failing_click_number:
                msg = "synthetic click failure"
                raise RuntimeError(msg)
            await super().click(x, y, warp=warp)

    async def sleep(_seconds: float) -> None:
        pass

    browser = FailingBrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_ROOM_TEMPLATE_PATH,
            settings_path=CREATE_ROOM_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_TEMPLATE_PATH,
            settings_path=CREATE_SETTINGS_PATH,
        ),
    )
    screen = HomeScreen(context=ScreenContext(browser=browser, rng=Random(0)))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(RuntimeError, match="synthetic click failure"):
        asyncio.run(screen.create_room())

    assert not screen._stale


def test_create_room_raises_if_friendly_match_button_is_missing() -> None:
    screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(screenshot)
    screen = HomeScreen(context=ScreenContext(browser=browser))

    with pytest.raises(
        ScreenDetectionError,
        match="friendly-match was not found",
    ) as exc_info:
        asyncio.run(screen.create_room())

    assert browser.clicked_points == []
    assert exc_info.value.screenshot == screenshot


def test_create_room_raises_if_create_room_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_create_room_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        missing_create_room_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="create-room was not found",
    ) as exc_info:
        asyncio.run(screen.create_room())

    assert len(browser.clicked_points) == 1
    assert sleeps == [1.0]
    assert exc_info.value.screenshot == missing_create_room_screenshot


def test_create_room_raises_if_create_button_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    missing_create_screenshot = _synthetic_blank_screenshot()
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
            settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
        ),
        _synthetic_template_screenshot(
            template_path=CREATE_ROOM_TEMPLATE_PATH,
            settings_path=CREATE_ROOM_SETTINGS_PATH,
        ),
        missing_create_screenshot,
    )
    screen = HomeScreen(context=ScreenContext(browser=browser))
    monkeypatch.setattr(home_module.asyncio, "sleep", sleep)

    with pytest.raises(
        ScreenDetectionError,
        match="create was not found after opening room creation",
    ) as exc_info:
        asyncio.run(screen.create_room())

    assert len(browser.clicked_points) == 2
    assert sleeps == [1.0, 1.0]
    assert exc_info.value.screenshot == missing_create_screenshot


def test_create_room_rejects_stale_home_screen() -> None:
    screenshot = _synthetic_blank_screenshot()
    screen = HomeScreen(
        context=ScreenContext(browser=BrowserControllerSpy(screenshot)),
    )
    screen._mark_stale()

    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(screen.create_room())

    assert exc_info.value.screenshot == screenshot


def test_create_room_template_assets_exist() -> None:
    assert CREATE_ROOM_TEMPLATE_PATH.name == "create-room.png"
    assert CREATE_ROOM_TEMPLATE_PATH.is_file()
    assert CREATE_ROOM_SETTINGS_PATH.name == "create-room.toml"
    assert CREATE_ROOM_SETTINGS_PATH.is_file()


def test_room_create_button_template_assets_exist() -> None:
    assert CREATE_TEMPLATE_PATH.name == "create.png"
    assert CREATE_TEMPLATE_PATH.is_file()
    assert CREATE_SETTINGS_PATH.name == "create.toml"
    assert CREATE_SETTINGS_PATH.is_file()
