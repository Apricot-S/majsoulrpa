import asyncio
from collections.abc import Awaitable, Callable, Mapping
from math import isfinite
from typing import Any, NoReturn, Protocol

from majsoulrpa._tasks import cancel_tasks, raise_task_errors
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen, ScreenContext
from majsoulrpa.screens.errors import ScreenDetectionTimeoutError
from majsoulrpa.types import Callback

type ScreenTypes = tuple[type[Screen], ...]
type Cleanup = Callable[[], Awaitable[None]]
type StopPredicate = Callable[[], bool]
type ScreenshotProvider = Callable[[], Awaitable[bytes]]
type BackgroundService = Callable[[], Awaitable[None]]
type BackgroundReady = Callable[[], Awaitable[object]]

SCREEN_DETECTION_RETRY_INTERVAL_SECONDS = 0.5


async def _noop() -> None:
    pass


def _keep_running() -> bool:
    return False


class ScreenDetector(Protocol):
    async def detect(self, screen_types: ScreenTypes) -> Screen | None: ...
    async def screenshot(self) -> bytes: ...


class ScreenshotScreenDetector:
    def __init__(
        self,
        screenshot: ScreenshotProvider,
        context: ScreenContext | None = None,
    ) -> None:
        self._screenshot = screenshot
        self._context = context

    async def detect(self, screen_types: ScreenTypes) -> Screen | None:
        screenshot = await self._screenshot()
        for screen_type in screen_types:
            if screen_type.detection_spec().matches(screenshot):
                return screen_type(context=self._context)
        return None

    async def screenshot(self) -> bytes:
        return await self._screenshot()


class RPARuntime:
    def __init__(
        self,
        callbacks: Mapping[type[Screen], Callback[Any]],
        detector: ScreenDetector,
        *,
        cleanup: Cleanup = _noop,
        should_stop: StopPredicate = _keep_running,
        background_service: BackgroundService | None = None,
        background_ready: BackgroundReady = _noop,
    ) -> None:
        self._callbacks = callbacks
        self._detector = detector
        self._cleanup = cleanup
        self._should_stop = should_stop
        self._background_service = background_service
        self._background_ready = background_ready

    async def run(
        self,
        data: Any,  # noqa: ANN401
        *,
        detection_timeout: float | None = None,
    ) -> Any:  # noqa: ANN401
        try:
            _validate_detection_timeout(detection_timeout)

            if self._background_service is None:
                result = await self._run_loop(data, detection_timeout)
            else:
                result = await self._run_with_background(
                    data,
                    detection_timeout,
                )
        except BaseException as error:
            try:
                await self._cleanup()
            except BaseException as cleanup_error:  # noqa: BLE001
                msg = "RPA runtime and cleanup failed."
                raise BaseExceptionGroup(msg, [error, cleanup_error]) from None
            raise
        else:
            await self._cleanup()
            return result

    async def _run_loop(
        self,
        data: Any,  # noqa: ANN401
        detection_timeout: float | None,
    ) -> Any:  # noqa: ANN401
        current_data = data
        screen_types = tuple(self._callbacks)

        while True:
            screen = await self._detect(screen_types, detection_timeout)

            callback = self._callbacks.get(type(screen))
            if callback is None:
                continue

            await screen.before_callback()
            current_data = await callback(screen, current_data)
            if self._should_stop():
                return current_data

    async def _run_with_background(
        self,
        data: Any,  # noqa: ANN401
        detection_timeout: float | None,
    ) -> Any:  # noqa: ANN401
        if self._background_service is None:
            msg = "Background service is not configured."
            raise RuntimeError(msg)
        main_task = asyncio.create_task(
            self._run_main_when_ready(data, detection_timeout),
        )
        background_task = asyncio.ensure_future(self._background_service())
        tasks = (main_task, background_task)
        try:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
        except BaseException as error:
            cancellation_errors = await cancel_tasks(tasks)
            if cancellation_errors:
                msg = "RPA runtime task cancellation failed."
                raise BaseExceptionGroup(
                    msg,
                    [error, *cancellation_errors],
                ) from None
            raise

        cancellation_errors = await cancel_tasks(pending)
        task_errors: list[BaseException] = []
        main_succeeded = False
        main_result: Any = None

        for task in tasks:
            if task not in done:
                continue

            try:
                result = task.result()
            except BaseException as error:  # noqa: BLE001
                task_errors.append(error)
            else:
                if task is main_task:
                    main_succeeded = True
                    main_result = result
                else:
                    msg = "RPA background service stopped unexpectedly."
                    task_errors.append(RuntimeError(msg))

        raise_task_errors(
            [*task_errors, *cancellation_errors],
            group_message="RPA runtime tasks failed.",
        )

        if not main_succeeded:
            msg = "RPA main task did not produce a result."
            raise RuntimeError(msg)
        return main_result

    async def _run_main_when_ready(
        self,
        data: Any,  # noqa: ANN401
        detection_timeout: float | None,
    ) -> Any:  # noqa: ANN401
        await self._background_ready()
        return await self._run_loop(data, detection_timeout)

    async def _detect(
        self,
        screen_types: ScreenTypes,
        detection_timeout: float | None,
    ) -> Screen:
        loop = asyncio.get_running_loop()
        deadline = (
            None
            if detection_timeout is None
            else loop.time() + detection_timeout
        )

        while True:
            timeout = None if deadline is None else deadline - loop.time()
            if timeout is not None and timeout <= 0:
                await self._raise_detection_timeout()

            try:
                async with asyncio.timeout(timeout):
                    screen = await self._detector.detect(screen_types)
            except TimeoutError:
                await self._raise_detection_timeout()
            if screen is not None:
                return screen

            if deadline is None:
                sleep_seconds = SCREEN_DETECTION_RETRY_INTERVAL_SECONDS
            else:
                sleep_seconds = min(
                    SCREEN_DETECTION_RETRY_INTERVAL_SECONDS,
                    max(0, deadline - loop.time()),
                )
                if sleep_seconds <= 0:
                    await self._raise_detection_timeout()

            await asyncio.sleep(sleep_seconds)

    async def _raise_detection_timeout(self) -> NoReturn:
        screenshot = await self._detector.screenshot()
        msg = "Screen detection timed out."
        raise ScreenDetectionTimeoutError(msg, screenshot)


def _validate_detection_timeout(detection_timeout: float | None) -> None:
    if detection_timeout is None:
        return
    if not isfinite(detection_timeout):
        msg = "detection_timeout must be finite."
        raise ValueError(msg)
    if detection_timeout <= 0:
        msg = "detection_timeout must be positive."
        raise ValueError(msg)


type RuntimeFactory = Callable[
    [Mapping[type[Screen], Callback[Any]], AppConfig],
    RPARuntime,
]
