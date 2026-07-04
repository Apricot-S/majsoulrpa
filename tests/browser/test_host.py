import asyncio

import pytest

from majsoulrpa.browser import BrowserHost
from majsoulrpa.config import AppConfig


class BrowserBackendSpy:
    def __init__(self) -> None:
        self.started = 0
        self.stopped = 0
        self.start_error: BaseException | None = None
        self.last_config: AppConfig | None = None

    async def start(self, config: AppConfig) -> None:
        self.started += 1
        self.last_config = config
        if self.start_error is not None:
            raise self.start_error

    async def stop(self) -> None:
        self.stopped += 1


def test_browser_host_is_running_after_start() -> None:
    backend = BrowserBackendSpy()
    host = BrowserHost(backend)

    asyncio.run(host.start(AppConfig()))

    assert host.is_running is True
    assert backend.started == 1


def test_browser_host_start_failure_is_propagated() -> None:
    backend = BrowserBackendSpy()
    backend.start_error = RuntimeError("failed to start")
    host = BrowserHost(backend)

    with pytest.raises(RuntimeError, match="failed to start"):
        asyncio.run(host.start(AppConfig()))


def test_browser_host_start_failure_does_not_mark_running() -> None:
    backend = BrowserBackendSpy()
    backend.start_error = RuntimeError("failed to start")
    host = BrowserHost(backend)

    with pytest.raises(RuntimeError, match="failed to start"):
        asyncio.run(host.start(AppConfig()))

    assert host.is_running is False


def test_browser_host_cleans_up_when_start_is_cancelled() -> None:
    backend = BrowserBackendSpy()
    backend.start_error = asyncio.CancelledError()
    host = BrowserHost(backend)

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(host.start(AppConfig()))

    assert host.is_running is False
    assert backend.stopped == 1


def test_browser_host_stop_marks_stopped() -> None:
    backend = BrowserBackendSpy()
    host = BrowserHost(backend)
    asyncio.run(host.start(AppConfig()))

    asyncio.run(host.stop())

    assert host.is_running is False
    assert backend.stopped == 1


def test_browser_host_stop_is_idempotent_after_stopped() -> None:
    backend = BrowserBackendSpy()
    host = BrowserHost(backend)
    asyncio.run(host.start(AppConfig()))

    asyncio.run(host.stop())
    asyncio.run(host.stop())

    assert host.is_running is False
    assert backend.stopped == 1
