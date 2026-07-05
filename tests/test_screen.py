import asyncio
from typing import override

from majsoulrpa.client import ScreenshotScreenDetector
from majsoulrpa.screens import Screen, ScreenDetectionSpec


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
