from typing import Any, cast

import pytest

from majsoulrpa import RPAApp


class LoginScreen:
    pass


class HomeScreen:
    pass


def test_rpa_app_registers_async_callback() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, state: object) -> object:
        return state

    assert app.registered_screen_types == (LoginScreen,)
    assert handle_login.__name__ == "handle_login"


def test_rpa_app_callback_state_may_change_type() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, state: int) -> str:
        return str(state)

    assert app.registered_screen_types == (LoginScreen,)
    assert handle_login.__name__ == "handle_login"


def test_rpa_app_rejects_sync_callback() -> None:
    app = RPAApp()

    def handle_login(_screen: LoginScreen, state: object) -> object:
        return state

    with pytest.raises(TypeError, match="must be async"):
        app.on(LoginScreen)(cast("Any", handle_login))


def test_rpa_app_rejects_duplicate_screen_registration() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, state: object) -> object:
        return state

    with pytest.raises(ValueError, match="already registered"):

        @app.on(LoginScreen)
        async def handle_login_again(
            _screen: LoginScreen,
            state: object,
        ) -> object:
            return state


def test_rpa_app_preserves_registration_order() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, state: object) -> object:
        return state

    @app.on(HomeScreen)
    async def handle_home(_screen: HomeScreen, state: object) -> object:
        return state

    assert app.registered_screen_types == (LoginScreen, HomeScreen)
