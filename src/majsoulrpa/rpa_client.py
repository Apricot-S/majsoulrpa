# ruff: noqa: ANN401

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from majsoulrpa import browser, constants
from majsoulrpa.presentation.base import Presentation

type Callback[P: Presentation] = Callable[[P, Any], Awaitable[Any]]


class RPAClient:
    @dataclass(frozen=True)
    class Config:
        address: str = constants.DEFAULT_CLIENT_ADDRESS
        port: int = constants.DEFAULT_REMOTE_PORT

    def __init__(self) -> None:
        self._callbacks: dict[
            type[Presentation],
            Callable[..., Awaitable[Any]],
        ] = {}

    async def _detect(self, driver: browser.DriverBase) -> Presentation:
        while True:
            for candidate in self._callbacks:
                p = await candidate._detect(driver)  # noqa: SLF001
                if p is not None:
                    return p
            await asyncio.sleep(0.5)

    async def _dispatch(self, presentation: Presentation, data: Any) -> Any:
        await presentation._pre_dispatch()  # noqa: SLF001
        return await self._callbacks[type(presentation)](presentation, data)

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
        detection_timeout: float = 30.0,
        browser_client: browser.ClientBase | None = None,
        browser_driver: browser.DriverBase | None = None,
    ) -> None:
        if not self._callbacks:
            msg = "no callbacks registered: use `RPAClient.on()` to register a Presentation callback"  # noqa: E501
            raise RuntimeError(msg)

        client = browser_client or browser.Client(config.address, config.port)
        driver = browser_driver or browser.Driver(client)

        async with client, driver:
            while True:
                async with asyncio.timeout(detection_timeout):
                    p = await self._detect(driver)

                data = await self._dispatch(p, data)

                if p._is_ended:  # noqa: SLF001
                    break
