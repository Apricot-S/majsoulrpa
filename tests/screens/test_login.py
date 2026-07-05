import pytest

from majsoulrpa.screens import LoginScreen, Screen, ScreenDetectionSpec


def test_login_screen_is_screen() -> None:
    assert issubclass(LoginScreen, Screen)


def test_login_screen_detection_spec_uses_template_predicate() -> None:
    spec = LoginScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    with pytest.raises(RuntimeError, match="template matcher"):
        spec.matches(object())
