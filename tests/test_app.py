import asyncio
from collections.abc import Mapping
from typing import Any, cast

import pytest

from majsoulrpa import RPAApp
from majsoulrpa.client import RPARuntime
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.types import Callback


class LoginScreen(Screen):
    @classmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class HomeScreen(Screen):
    @classmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class UnknownScreen(Screen):
    @classmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class SequenceScreenDetector:
    def __init__(self, *screens: Screen | None) -> None:
        self._screens = list(screens)
        self.seen_screen_types: list[tuple[type[Screen], ...]] = []

    async def detect(
        self,
        screen_types: tuple[type[Screen], ...],
    ) -> Screen | None:
        self.seen_screen_types.append(screen_types)
        if not self._screens:
            return None
        return self._screens.pop(0)


class BlockingScreenDetector:
    async def detect(
        self,
        screen_types: tuple[type[Screen], ...],
    ) -> Screen | None:
        _ = screen_types
        await asyncio.Event().wait()


class CleanupSpy:
    def __init__(self) -> None:
        self.called = 0

    async def __call__(self) -> None:
        self.called += 1


class RuntimeFactorySpy:
    def __init__(
        self,
        detector: SequenceScreenDetector | BlockingScreenDetector,
        cleanup: CleanupSpy | None = None,
    ) -> None:
        self._detector = detector
        self._cleanup = cleanup

    def __call__(
        self,
        callbacks: Mapping[type[Screen], Callback[Any]],
    ) -> RPARuntime:
        return RPARuntime(callbacks, self._detector, cleanup=self._cleanup)


def test_rpa_app_registers_async_callback() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: object) -> object:
        return data

    assert app.registered_screen_types == (LoginScreen,)
    assert handle_login.__name__ == "handle_login"


def test_rpa_app_callback_data_may_change_type() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: int) -> str:
        return str(data)

    assert app.registered_screen_types == (LoginScreen,)
    assert handle_login.__name__ == "handle_login"


def test_rpa_app_rejects_sync_callback() -> None:
    app = RPAApp()

    def handle_login(_screen: LoginScreen, data: object) -> object:
        return data

    with pytest.raises(TypeError, match="must be async"):
        app.on(LoginScreen)(cast("Any", handle_login))


def test_rpa_app_rejects_duplicate_screen_registration() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: object) -> object:
        return data

    with pytest.raises(ValueError, match="already registered"):

        @app.on(LoginScreen)
        async def handle_login_again(
            _screen: LoginScreen,
            data: object,
        ) -> object:
            return data


def test_rpa_app_preserves_registration_order() -> None:
    app = RPAApp()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: object) -> object:
        return data

    @app.on(HomeScreen)
    async def handle_home(_screen: HomeScreen, data: object) -> object:
        return data

    assert app.registered_screen_types == (LoginScreen, HomeScreen)


def test_rpa_app_run_dispatches_registered_screen() -> None:
    detector = SequenceScreenDetector(LoginScreen(), None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: int) -> int:
        return data + 1

    data = asyncio.run(app.run(AppConfig(), 1))

    assert data == 2


def test_rpa_app_run_ignores_unregistered_screen() -> None:
    detector = SequenceScreenDetector(UnknownScreen(), LoginScreen(), None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: int) -> int:
        return data + 1

    data = asyncio.run(app.run(AppConfig(), 1))

    assert data == 2


def test_rpa_app_run_returns_callback_data() -> None:
    detector = SequenceScreenDetector(LoginScreen(), None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: int) -> str:
        return str(data)

    data = asyncio.run(app.run(AppConfig(), 123))

    assert data == "123"


def test_rpa_app_run_propagates_callback_exception() -> None:
    detector = SequenceScreenDetector(LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        msg = "callback failed"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="callback failed"):
        asyncio.run(app.run(AppConfig(), None))


def test_rpa_app_run_raises_detection_timeout() -> None:
    app = RPAApp(runtime_factory=RuntimeFactorySpy(BlockingScreenDetector()))

    with pytest.raises(TimeoutError):
        asyncio.run(app.run(AppConfig(), None, detection_timeout=0.001))


def test_rpa_app_run_cleans_up_when_callback_is_cancelled() -> None:
    cleanup = CleanupSpy()
    detector = SequenceScreenDetector(LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector, cleanup))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(app.run(AppConfig(), None))

    assert cleanup.called == 1
