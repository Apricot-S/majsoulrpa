# ruff: noqa: ANN401

import asyncio
import warnings
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from logging import getLogger
from typing import Any

from majsoulrpa import browser, sniffer
from majsoulrpa.exceptions import UserInputError
from majsoulrpa.netutils import UserPort
from majsoulrpa.presentation.base import Presentation
from majsoulrpa.presentation.exceptions import PresentationTimeoutError

logger = getLogger(__name__)

type Callback[P: Presentation] = Callable[[P, Any], Awaitable[Any]]


@dataclass(frozen=True)
class Config:
    browser_address: IPv4Address | IPv6Address
    remote_port: UserPort
    sniffer_port: UserPort

    def __post_init__(self) -> None:
        ports = [self.remote_port, self.sniffer_port]
        if len(set(ports)) != len(ports):
            msg = "port number conflict"
            raise UserInputError(msg)


class RPAClient:
    def __init__(self) -> None:
        self._callbacks: dict[
            type[Presentation],
            Callable[..., Awaitable[Any]],
        ] = {}

    async def _detect(
        self,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> Presentation:
        logger.debug("Detecting presentation candidates...")
        while True:
            for candidate in self._callbacks:
                p = await candidate._detect(driver, message_queue)  # noqa: SLF001
                if p is not None:
                    logger.info("Detected presentation `%s`", type(p).__name__)
                    return p
            await asyncio.sleep(0.5)

    async def _dispatch(self, presentation: Presentation, data: Any) -> Any:
        await presentation._pre_dispatch()  # noqa: SLF001
        callback = self._callbacks[type(presentation)](presentation, data)

        logger.debug(
            "Dispatching callback for `%s`",
            type(presentation).__name__,
        )
        ret = await callback

        logger.debug(
            "Callback for `%s` completed",
            type(presentation).__name__,
        )
        return ret

    def on[P: Presentation](
        self,
        presentation_cls: type[P],
    ) -> Callable[[Callback[P]], Callback[P]]:
        def decorator(callback: Callback[P]) -> Callback[P]:
            self._callbacks[presentation_cls] = callback
            return callback

        return decorator

    async def run(
        self,
        config: Config,
        data: Any,
        detection_timeout: float = 60.0,
        browser_client: browser.ClientBase | None = None,
        browser_driver: browser.DriverBase | None = None,
        message_queue: sniffer.MessageQueueBase | None = None,
    ) -> Any:
        if not self._callbacks:
            msg = "no callbacks registered: use `RPAClient.on()` to register a presentation callback"  # noqa: E501
            raise RuntimeError(msg)

        # On Windows, the `ProactorEventLoop` does not implement
        # the add_reader family of methods.
        # When using `zmq.asyncio`, Tornado automatically registers
        # a selector thread to provide add_reader support.
        # This behavior always triggers a `RuntimeWarning`,
        # even though it is harmless.
        # Since Tornado is functioning correctly and the warning only
        # causes confusion, we suppress it here to keep the output
        # clean.
        warnings.filterwarnings(
            "ignore",
            message="Proactor event loop does not implement add_reader",
            category=RuntimeWarning,
            module="zmq",
        )

        if browser_client is None:
            browser_client = browser.Client(
                config.browser_address,
                config.remote_port,
            )
        if browser_driver is None:
            browser_driver = browser.Driver(browser_client)
        if message_queue is None:
            message_queue = sniffer.MessageQueue(
                config.browser_address,
                config.sniffer_port,
            )

        async with (
            browser_client,
            browser_driver,
            message_queue,
            asyncio.TaskGroup() as tg,
        ):
            message_queue_task = tg.create_task(message_queue.run())

            logger.info("RPA session started.")
            p: Presentation | None = None
            while True:
                if p is None or p._is_presentation_finished:  # noqa: SLF001
                    try:
                        async with asyncio.timeout(detection_timeout):
                            p = await self._detect(
                                browser_driver,
                                message_queue,
                            )
                    except TimeoutError as e:
                        msg = "presentation detection timed out."
                        ss = await browser_driver.get_screenshot()
                        raise PresentationTimeoutError(msg, ss) from e

                data = await self._dispatch(p, data)

                if p._is_rpa_ended:  # noqa: SLF001
                    logger.info("RPA session ended successfully.")
                    message_queue_task.cancel()
                    return data
