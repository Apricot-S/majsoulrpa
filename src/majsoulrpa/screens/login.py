from typing import override

from majsoulrpa.screens.base import Screen, ScreenDetectionSpec


def _login_template_matches(_screenshot: object) -> bool:
    msg = "LoginScreen template matcher is not configured."
    raise RuntimeError(msg)


class LoginScreen(Screen):
    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=_login_template_matches)
