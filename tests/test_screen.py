from majsoulrpa.screens import Screen, ScreenDetectionSpec


class LoginScreen(Screen):
    detection = ScreenDetectionSpec()


def test_screen_exposes_detection_spec() -> None:
    assert LoginScreen.detection_spec() is LoginScreen.detection


def test_screen_detection_spec_is_optional() -> None:
    assert Screen.detection_spec() is None
