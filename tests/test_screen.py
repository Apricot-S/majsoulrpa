import asyncio
from collections.abc import Mapping
from typing import Any, override

from majsoulrpa import RPAApp
from majsoulrpa.client import ScreenshotScreenDetector
from majsoulrpa.client.runtime import RPARuntime
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.types import Callback


class LoginScreen(Screen):
    spec = ScreenDetectionSpec()

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return cls.spec


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
    result = asyncio.run(app.run(AppConfig(), data))

    assert result is data
    assert called is False
