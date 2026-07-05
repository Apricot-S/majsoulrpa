from majsoulrpa.screens import Screen, ScreenDetectionSpec


class LoginScreen(Screen):
    spec = ScreenDetectionSpec()

    @classmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        return cls.spec


def test_screen_exposes_detection_spec() -> None:
    assert LoginScreen.detection_spec() is LoginScreen.spec


def test_screen_requires_detection_spec() -> None:
    assert Screen.__abstractmethods__ == frozenset({"detection_spec"})
