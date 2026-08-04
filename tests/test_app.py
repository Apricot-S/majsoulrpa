import asyncio
from collections.abc import Mapping
from typing import Any, cast, override

import pytest

import majsoulrpa.client.runtime as runtime_module
from majsoulrpa import RPAApp
from majsoulrpa.client.runtime import Cleanup, RPARuntime
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.screens.errors import ScreenDetectionTimeoutError
from majsoulrpa.types import Callback

SYNTHETIC_PNG = b"\x89PNG\r\n\x1a\n"


class LoginScreen(Screen):
    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class HomeScreen(Screen):
    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class UnknownScreen(Screen):
    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec()


class SequenceScreenDetector:
    def __init__(self, *screens: Screen | None) -> None:
        self._screens = list(screens)
        self.seen_screen_types: list[tuple[type[Screen], ...]] = []
        self.screenshot_bytes = SYNTHETIC_PNG
        self.detected_count = 0

    async def detect(
        self,
        screen_types: tuple[type[Screen], ...],
    ) -> Screen | None:
        self.seen_screen_types.append(screen_types)
        if not self._screens:
            return None
        screen = self._screens.pop(0)
        if screen is not None:
            self.detected_count += 1
        return screen

    async def screenshot(self) -> bytes:
        return self.screenshot_bytes

    def has_detected_screen(self) -> bool:
        return self.detected_count > 0


class BlockingScreenDetector:
    screenshot_bytes = SYNTHETIC_PNG

    async def detect(
        self,
        screen_types: tuple[type[Screen], ...],
    ) -> Screen | None:
        _ = screen_types
        await asyncio.Event().wait()

    async def screenshot(self) -> bytes:
        return self.screenshot_bytes


class UnexpectedScreenDetector:
    async def detect(
        self,
        screen_types: tuple[type[Screen], ...],
    ) -> Screen | None:
        _ = screen_types
        msg = "Screen detection must not start."
        raise AssertionError(msg)

    async def screenshot(self) -> bytes:
        msg = "A screenshot must not be requested."
        raise AssertionError(msg)


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
        cleanup: Cleanup | None = None,
    ) -> None:
        self._detector = detector
        self._cleanup = cleanup

    def __call__(
        self,
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        _ = config
        if not isinstance(self._detector, SequenceScreenDetector):
            if self._cleanup is None:
                return RPARuntime(callbacks, self._detector)
            return RPARuntime(
                callbacks,
                self._detector,
                cleanup=self._cleanup,
            )
        if self._cleanup is None:
            return RPARuntime(
                callbacks,
                self._detector,
                should_stop=self._detector.has_detected_screen,
            )
        return RPARuntime(
            callbacks,
            self._detector,
            cleanup=self._cleanup,
            should_stop=self._detector.has_detected_screen,
        )


class FalseyRuntimeFactory(RuntimeFactorySpy):
    def __bool__(self) -> bool:
        return False


class FalseyStopPredicate:
    def __init__(self) -> None:
        self.called = 0

    def __bool__(self) -> bool:
        return False

    def __call__(self) -> bool:
        self.called += 1
        return True


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


def test_rpa_app_run_uses_falsey_runtime_factory() -> None:
    detector = SequenceScreenDetector(LoginScreen(), None)
    factory = FalseyRuntimeFactory(detector)
    app = RPAApp(runtime_factory=factory)

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


def test_rpa_app_run_raises_detection_timeout_with_screenshot() -> None:
    detector = SequenceScreenDetector(None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector))

    with pytest.raises(ScreenDetectionTimeoutError) as exc_info:
        asyncio.run(app.run(AppConfig(), object(), detection_timeout=0.001))

    assert exc_info.value.screenshot == SYNTHETIC_PNG


def test_rpa_app_run_cleans_up_when_detection_timeout_expires() -> None:
    cleanup = CleanupSpy()
    detector = SequenceScreenDetector(None)
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector, cleanup))

    with pytest.raises(ScreenDetectionTimeoutError):
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


def test_rpa_app_run_preserves_callback_and_cleanup_failures() -> None:
    async def fail_cleanup() -> None:
        msg = "cleanup failed"
        raise ValueError(msg)

    detector = SequenceScreenDetector(LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector, fail_cleanup))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        msg = "callback failed"
        raise RuntimeError(msg)

    with pytest.raises(ExceptionGroup) as exc_info:
        asyncio.run(app.run(AppConfig(), None))

    callback_error, cleanup_error = exc_info.value.exceptions
    assert isinstance(callback_error, RuntimeError)
    assert str(callback_error) == "callback failed"
    assert isinstance(cleanup_error, ValueError)
    assert str(cleanup_error) == "cleanup failed"


def test_rpa_app_run_raises_detection_timeout() -> None:
    app = RPAApp(runtime_factory=RuntimeFactorySpy(BlockingScreenDetector()))

    with pytest.raises(ScreenDetectionTimeoutError) as exc_info:
        asyncio.run(app.run(AppConfig(), None, detection_timeout=0.001))

    assert exc_info.value.screenshot == SYNTHETIC_PNG


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


def test_rpa_app_run_preserves_cancellation_and_cleanup_failure() -> None:
    async def fail_cleanup() -> None:
        msg = "cleanup failed"
        raise RuntimeError(msg)

    detector = SequenceScreenDetector(LoginScreen())
    app = RPAApp(runtime_factory=RuntimeFactorySpy(detector, fail_cleanup))

    @app.on(LoginScreen)
    async def handle_login(_screen: LoginScreen, _data: object) -> object:
        raise asyncio.CancelledError

    with pytest.raises(BaseExceptionGroup) as exc_info:
        asyncio.run(app.run(AppConfig(), None))

    cancellation, cleanup_error = exc_info.value.exceptions
    assert isinstance(cancellation, asyncio.CancelledError)
    assert isinstance(cleanup_error, RuntimeError)
    assert str(cleanup_error) == "cleanup failed"


def test_rpa_runtime_propagates_background_service_failure() -> None:
    cleanup = CleanupSpy()

    async def fail() -> None:
        await asyncio.sleep(0)
        msg = "sniffer failed"
        raise RuntimeError(msg)

    runtime = RPARuntime(
        {},
        BlockingScreenDetector(),
        cleanup=cleanup,
        background_service=fail,
    )

    with pytest.raises(RuntimeError, match="sniffer failed"):
        asyncio.run(runtime.run(None))

    assert cleanup.called == 1


def test_rpa_runtime_preserves_background_and_cleanup_failures() -> None:
    async def fail_background_service() -> None:
        await asyncio.sleep(0)
        msg = "sniffer failed"
        raise RuntimeError(msg)

    async def fail_cleanup() -> None:
        msg = "cleanup failed"
        raise ValueError(msg)

    runtime = RPARuntime(
        {},
        BlockingScreenDetector(),
        cleanup=fail_cleanup,
        background_service=fail_background_service,
    )

    with pytest.raises(ExceptionGroup) as exc_info:
        asyncio.run(runtime.run(None))

    background_error, cleanup_error = exc_info.value.exceptions
    assert isinstance(background_error, RuntimeError)
    assert str(background_error) == "sniffer failed"
    assert isinstance(cleanup_error, ValueError)
    assert str(cleanup_error) == "cleanup failed"


def test_rpa_runtime_cancels_main_when_background_call_fails() -> None:
    def fail_background_call() -> asyncio.Future[None]:
        msg = "background call failed"
        raise RuntimeError(msg)

    runtime = RPARuntime(
        {},
        BlockingScreenDetector(),
        background_service=fail_background_call,
    )

    async def run_and_check_tasks() -> None:
        tasks_before = asyncio.all_tasks()
        with pytest.raises(RuntimeError, match="background call failed"):
            await runtime.run(None)
        assert asyncio.all_tasks() == tasks_before

    asyncio.run(run_and_check_tasks())


def test_rpa_runtime_cancels_main_when_background_task_creation_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def background_service() -> asyncio.Future[None]:
        return asyncio.Future()

    def fail_task_creation(_awaitable: object) -> asyncio.Future[None]:
        msg = "background task creation failed"
        raise RuntimeError(msg)

    monkeypatch.setattr(
        runtime_module.asyncio,
        "ensure_future",
        fail_task_creation,
    )
    runtime = RPARuntime(
        {},
        BlockingScreenDetector(),
        background_service=background_service,
    )

    async def run_and_check_tasks() -> None:
        tasks_before = asyncio.all_tasks()
        with pytest.raises(
            RuntimeError,
            match="background task creation failed",
        ):
            await runtime.run(None)
        assert asyncio.all_tasks() == tasks_before

    asyncio.run(run_and_check_tasks())


def test_rpa_runtime_cancels_background_service_after_normal_stop() -> None:
    cancelled = False

    async def run_until_cancelled() -> None:
        nonlocal cancelled
        try:
            await asyncio.Future()
        finally:
            cancelled = True

    runtime = RPARuntime(
        {LoginScreen: _return_data},
        SequenceScreenDetector(LoginScreen()),
        should_stop=lambda: True,
        background_service=run_until_cancelled,
    )

    result = asyncio.run(runtime.run("done"))

    assert result == "done"
    assert cancelled


def test_rpa_runtime_reports_background_cancellation_failure() -> None:
    async def fail_when_cancelled() -> None:
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            msg = "background cancellation failed"
            raise RuntimeError(msg) from None

    runtime = RPARuntime(
        {LoginScreen: _return_data},
        SequenceScreenDetector(LoginScreen()),
        should_stop=lambda: True,
        background_service=fail_when_cancelled,
    )

    with pytest.raises(RuntimeError, match="background cancellation failed"):
        asyncio.run(runtime.run("done"))


def test_rpa_runtime_preserves_main_cancellation_failure() -> None:
    detect_started = asyncio.Event()

    class CancellationFailingDetector:
        async def detect(
            self,
            screen_types: tuple[type[Screen], ...],
        ) -> Screen | None:
            _ = screen_types
            detect_started.set()
            try:
                await asyncio.Future()
            except asyncio.CancelledError:
                msg = "main cancellation failed"
                raise ValueError(msg) from None

        async def screenshot(self) -> bytes:
            return SYNTHETIC_PNG

    async def fail_background_service() -> None:
        await detect_started.wait()
        msg = "background failed"
        raise RuntimeError(msg)

    runtime = RPARuntime(
        {},
        CancellationFailingDetector(),
        background_service=fail_background_service,
    )

    with pytest.raises(ExceptionGroup) as exc_info:
        asyncio.run(runtime.run(None))

    background_error, cancellation_error = exc_info.value.exceptions
    assert isinstance(background_error, RuntimeError)
    assert str(background_error) == "background failed"
    assert isinstance(cancellation_error, ValueError)
    assert str(cancellation_error) == "main cancellation failed"


def test_rpa_runtime_preserves_child_failure_when_cancelled() -> None:
    background_started = asyncio.Event()

    async def fail_when_cancelled() -> None:
        background_started.set()
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            msg = "background cancellation failed"
            raise RuntimeError(msg) from None

    runtime = RPARuntime(
        {},
        BlockingScreenDetector(),
        background_service=fail_when_cancelled,
    )

    async def cancel_runtime() -> None:
        task = asyncio.create_task(runtime.run(None))
        await background_started.wait()
        task.cancel()
        await task

    with pytest.raises(BaseExceptionGroup) as exc_info:
        asyncio.run(cancel_runtime())

    cancellation, background_error = exc_info.value.exceptions
    assert isinstance(cancellation, asyncio.CancelledError)
    assert isinstance(background_error, RuntimeError)
    assert str(background_error) == "background cancellation failed"


def test_rpa_runtime_rejects_background_service_normal_exit() -> None:
    async def stop_unexpectedly() -> None:
        await asyncio.sleep(0)

    runtime = RPARuntime(
        {},
        BlockingScreenDetector(),
        background_service=stop_unexpectedly,
    )

    with pytest.raises(RuntimeError, match="stopped unexpectedly"):
        asyncio.run(runtime.run(None))


def test_rpa_runtime_waits_for_background_ready_before_main_loop() -> None:
    ready = asyncio.Event()
    detector = SequenceScreenDetector(LoginScreen())

    async def background() -> None:
        assert detector.detected_count == 0
        ready.set()
        await asyncio.Future()

    runtime = RPARuntime(
        {LoginScreen: _return_data},
        detector,
        should_stop=lambda: True,
        background_service=background,
        background_ready=ready.wait,
    )

    result = asyncio.run(runtime.run("done"))

    assert result == "done"


@pytest.mark.parametrize(
    "detection_timeout",
    [0.0, -0.1, float("nan"), float("inf"), float("-inf")],
)
def test_rpa_runtime_rejects_invalid_detection_timeout(
    detection_timeout: float,
) -> None:
    runtime = RPARuntime({}, UnexpectedScreenDetector())

    with pytest.raises(ValueError, match="detection_timeout"):
        asyncio.run(
            runtime.run(None, detection_timeout=detection_timeout),
        )


def test_rpa_runtime_uses_falsey_stop_predicate() -> None:
    should_stop = FalseyStopPredicate()

    async def fail_if_dispatched(
        _screen: UnknownScreen,
        _data: object,
    ) -> object:
        msg = "Runtime did not use the configured stop predicate."
        raise AssertionError(msg)

    runtime = RPARuntime(
        {LoginScreen: _return_data, UnknownScreen: fail_if_dispatched},
        SequenceScreenDetector(LoginScreen(), UnknownScreen()),
        should_stop=should_stop,
    )

    result = asyncio.run(runtime.run("data"))

    assert result == "data"
    assert should_stop.called == 1


async def _return_data(_screen: LoginScreen, data: object) -> object:
    return data
