import asyncio
from collections.abc import Awaitable, Callable, Mapping
from typing import Any, NoReturn, Protocol

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
        cleanup: Cleanup | None = None,
        should_stop: StopPredicate | None = None,
        background_service: BackgroundService | None = None,
        background_ready: BackgroundReady | None = None,
    ) -> None:
        self._callbacks = callbacks
        self._detector = detector
        self._cleanup = cleanup
        self._should_stop = should_stop or _keep_running
        self._background_service = background_service
        self._background_ready = background_ready

    async def run(
        self,
        config: AppConfig,
        data: Any,  # noqa: ANN401
        *,
        detection_timeout: float | None = None,
    ) -> Any:  # noqa: ANN401
        _ = config
        try:
            if self._background_service is None:
                return await self._run_loop(data, detection_timeout)
            return await self._run_with_background(data, detection_timeout)
        finally:
            await self._run_cleanup()

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
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            if background_task.done():
                main_task.cancel()
                await asyncio.gather(main_task, return_exceptions=True)
                if background_task.exception() is None:
                    msg = "RPA background service stopped unexpectedly."
                    raise RuntimeError(msg)
                # The background service has no result value. This call
                # re-raises its exception; only the main task returns
                # RPA data.
                return background_task.result()

            background_task.cancel()
            await asyncio.gather(background_task, return_exceptions=True)
            return main_task.result()
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _run_main_when_ready(
        self,
        data: Any,  # noqa: ANN401
        detection_timeout: float | None,
    ) -> Any:  # noqa: ANN401
        if self._background_ready is not None:
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

    async def _run_cleanup(self) -> None:
        if self._cleanup is None:
            return

        await self._cleanup()


type RuntimeFactory = Callable[
    [Mapping[type[Screen], Callback[Any]], AppConfig],
    RPARuntime,
]


def _keep_running() -> bool:
    return False
