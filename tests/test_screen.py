import asyncio
from collections.abc import Mapping
from typing import Any, override

import pytest

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

    result = asyncio.run(app.run(AppConfig(), None))

    assert result == "first"
