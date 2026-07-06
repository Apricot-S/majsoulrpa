import asyncio
from collections.abc import Mapping
from random import Random
from typing import Any, override

import pytest

import majsoulrpa.screens.base as screens_base
from majsoulrpa import RPAApp
from majsoulrpa.client import ScreenshotScreenDetector
from majsoulrpa.client.runtime import RPARuntime
from majsoulrpa.config import AppConfig
from majsoulrpa.presentation import Region
from majsoulrpa.screens import Screen, ScreenContext, ScreenDetectionSpec
from majsoulrpa.types import Callback


class LoginScreen(Screen):
    spec = ScreenDetectionSpec()

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return cls.spec


class BrowserControllerSpy:
    def __init__(self) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.input_texts: list[str] = []
        self.events: list[str] = []
        self.screenshot_bytes = b"\x89PNG\r\n\x1a\n"

    async def click(self, x: float, y: float) -> None:
        self.clicked_points.append((x, y))
        self.events.append("click")

    async def input_text(self, text: str) -> None:
        self.input_texts.append(text)
        self.events.append("input_text")

    async def screenshot(self) -> bytes:
        self.events.append("screenshot")
        return self.screenshot_bytes


def test_screen_exposes_detection_spec() -> None:
    assert LoginScreen.detection_spec() is LoginScreen.spec


def test_screen_requires_detection_spec() -> None:
    assert Screen.__abstractmethods__ == frozenset({"detection_spec"})


def test_screen_detector_detects_screen_from_fake_screenshot() -> None:
    class FakeScreenshot:
        marker = "login"

    def matches_login(screenshot: object) -> bool:
        return (
            isinstance(screenshot, FakeScreenshot)
            and screenshot.marker == "login"
        )

    class FakeLoginScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=matches_login)

    async def screenshot() -> FakeScreenshot:
        return FakeScreenshot()

    detector = ScreenshotScreenDetector(screenshot)

    screen = asyncio.run(detector.detect((FakeLoginScreen,)))

    assert isinstance(screen, FakeLoginScreen)


def test_screen_detector_injects_context_into_detected_screen() -> None:
    class FakeScreenshot:
        marker = "login"

    def matches_login(screenshot: object) -> bool:
        return (
            isinstance(screenshot, FakeScreenshot)
            and screenshot.marker == "login"
        )

    class FakeLoginScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=matches_login)

    async def screenshot() -> FakeScreenshot:
        return FakeScreenshot()

    context = ScreenContext(browser=BrowserControllerSpy())
    detector = ScreenshotScreenDetector(screenshot, context=context)

    screen = asyncio.run(detector.detect((FakeLoginScreen,)))

    assert isinstance(screen, FakeLoginScreen)
    assert screen.context is context


def test_screen_context_is_required_before_screen_operation() -> None:
    screen = LoginScreen()

    with pytest.raises(RuntimeError, match="ScreenContext"):
        _ = screen.context


def test_false_screen_detection_does_not_call_callback() -> None:
    class FakeScreenshot:
        pass

    class NeverScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=lambda _screenshot: False)

    async def screenshot() -> FakeScreenshot:
        return FakeScreenshot()

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
    ) -> RPARuntime:
        return RPARuntime(callbacks, ScreenshotScreenDetector(screenshot))

    app = RPAApp(runtime_factory=runtime_factory)
    called = False

    @app.on(NeverScreen)
    async def handle_never(_screen: NeverScreen, data: object) -> object:
        nonlocal called
        called = True
        return data

    data = object()
    result = asyncio.run(app.run(AppConfig(), data, detection_timeout=0.001))

    assert result is data
    assert called is False


def test_screen_detection_exception_is_not_hidden() -> None:
    class FakeScreenshot:
        pass

    def raise_detection_error(_screenshot: object) -> bool:
        msg = "detection failed"
        raise RuntimeError(msg)

    class BrokenScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(predicate=raise_detection_error)

    async def screenshot() -> FakeScreenshot:
        return FakeScreenshot()

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
    ) -> RPARuntime:
        return RPARuntime(callbacks, ScreenshotScreenDetector(screenshot))

    app = RPAApp(runtime_factory=runtime_factory)

    @app.on(BrokenScreen)
    async def handle_broken(_screen: BrokenScreen, data: object) -> object:
        return data

    with pytest.raises(RuntimeError, match="detection failed"):
        asyncio.run(app.run(AppConfig(), object()))


def test_multiple_matching_screens_use_registration_order() -> None:
    class FakeScreenshot:
        def __init__(self, *, matches: bool) -> None:
            self.matches = matches

    class FirstScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(
                predicate=lambda screenshot: (
                    isinstance(screenshot, FakeScreenshot)
                    and screenshot.matches
                ),
            )

    class SecondScreen(Screen):
        @classmethod
        @override
        def detection_spec(cls) -> ScreenDetectionSpec:
            return ScreenDetectionSpec(
                predicate=lambda screenshot: (
                    isinstance(screenshot, FakeScreenshot)
                    and screenshot.matches
                ),
            )

    screenshots = [FakeScreenshot(matches=True), FakeScreenshot(matches=False)]

    async def screenshot() -> FakeScreenshot:
        if not screenshots:
            return FakeScreenshot(matches=False)
        return screenshots.pop(0)

    def runtime_factory(
        callbacks: Mapping[type[Screen], Callback[Any]],
    ) -> RPARuntime:
        return RPARuntime(callbacks, ScreenshotScreenDetector(screenshot))

    app = RPAApp(runtime_factory=runtime_factory)

    @app.on(FirstScreen)
    async def handle_first(_screen: FirstScreen, _data: object) -> str:
        return "first"

    @app.on(SecondScreen)
    async def handle_second(_screen: SecondScreen, _data: object) -> str:
        return "second"

    result = asyncio.run(app.run(AppConfig(), None, detection_timeout=0.001))

    assert result == "first"


def test_screen_fills_scaled_region(monkeypatch: pytest.MonkeyPatch) -> None:
    browser = BrowserControllerSpy()
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        browser.events.append("sleep")

    screen = LoginScreen(
        context=ScreenContext(
            browser=browser,
            viewport_width=1280,
            viewport_height=720,
            rng=Random(0),
        ),
    )

    monkeypatch.setattr(screens_base.asyncio, "sleep", sleep)

    asyncio.run(
        screen.fill_region(
            Region(left=300, top=150, width=6, height=3),
            "player@example.invalid",
        ),
    )

    [(x, y)] = browser.clicked_points
    assert 200 < x < 204
    assert 100 < y < 102
    assert sleeps == [0.5]
    assert browser.events == ["click", "sleep", "input_text"]
    assert browser.input_texts == ["player@example.invalid"]


def test_screen_context_requests_stop() -> None:
    requested = False

    async def request_stop() -> None:
        nonlocal requested
        requested = True

    context = ScreenContext(
        browser=BrowserControllerSpy(),
        request_stop=request_stop,
    )

    asyncio.run(context.request_stop())

    assert requested is True


def test_screen_context_browser_can_take_screenshot() -> None:
    browser = BrowserControllerSpy()
    context = ScreenContext(browser=browser)

    screenshot = asyncio.run(context.browser.screenshot())

    assert screenshot == b"\x89PNG\r\n\x1a\n"
    assert browser.events == ["screenshot"]
