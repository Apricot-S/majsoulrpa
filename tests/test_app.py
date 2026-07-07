import asyncio
from collections.abc import Mapping
from typing import Any, cast, override

import pytest

import majsoulrpa.client.runtime as runtime_module
from majsoulrpa import RPAApp
from majsoulrpa.client import RPARuntime
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.types import Callback


class LoginScreen(Screen):
    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class HomeScreen(Screen):
    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class UnknownScreen(Screen):
    @classmethod
    @override
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


class UnrepresentableData:
    def __repr__(self) -> str:
        msg = "data must not be represented"
        raise AssertionError(msg)


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
        config: AppConfig,
    ) -> RPARuntime:
        _ = config
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

    data = asyncio.run(app.run(AppConfig(), 1, detection_timeout=0.001))

    assert data == 2


def test_rpa_app_run_ignores_unregistered_screen() -> None:
    detector = SequenceScreenDetector(UnknownScreen(), LoginScreen(), None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: int) -> int:
        return data + 1

    data = asyncio.run(app.run(AppConfig(), 1, detection_timeout=0.001))

    assert data == 2


def test_rpa_app_run_returns_callback_data() -> None:
    detector = SequenceScreenDetector(LoginScreen(), None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: int) -> str:
        return str(data)

    data = asyncio.run(app.run(AppConfig(), 123, detection_timeout=0.001))

    assert data == "123"


def test_rpa_app_run_does_not_represent_data() -> None:
    detector = SequenceScreenDetector(LoginScreen(), None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))
    data_in = UnrepresentableData()

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, data: object) -> object:
        assert data is data_in
        return data

    data_out = asyncio.run(
        app.run(AppConfig(), data_in, detection_timeout=0.001),
    )

    assert data_out is data_in


def test_rpa_app_run_retries_screen_detection_until_screen_is_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    detector = SequenceScreenDetector(None, None, LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(runtime_module.asyncio, "sleep", sleep)

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        msg = "stop after detected"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="stop after detected"):
        asyncio.run(app.run(AppConfig(), None))

    assert sleeps == [0.5, 0.5]
    assert detector.seen_screen_types == [
        (LoginScreen,),
        (LoginScreen,),
        (LoginScreen,),
    ]


def test_rpa_app_run_returns_data_when_detection_timeout_expires() -> None:
    detector = SequenceScreenDetector(None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))
    data = object()

    result = asyncio.run(app.run(AppConfig(), data, detection_timeout=0.001))

    assert result is data


def test_rpa_app_run_cleans_up_when_detection_timeout_expires() -> None:
    cleanup = CleanupSpy()
    detector = SequenceScreenDetector(None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector, cleanup))

    asyncio.run(app.run(AppConfig(), None, detection_timeout=0.001))

    assert cleanup.called == 1


def test_rpa_app_run_propagates_callback_exception() -> None:
    detector = SequenceScreenDetector(LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        msg = "callback failed"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="callback failed"):
        asyncio.run(app.run(AppConfig(), None))


def test_rpa_app_run_cleans_up_when_callback_fails() -> None:
    cleanup = CleanupSpy()
    detector = SequenceScreenDetector(LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector, cleanup))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        msg = "callback failed"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="callback failed"):
        asyncio.run(app.run(AppConfig(), None))

    assert cleanup.called == 1


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
