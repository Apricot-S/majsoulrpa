# ruff: noqa: ANN401

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from majsoulrpa import browser
from majsoulrpa.presentation.base import Presentation
from majsoulrpa.presentation.login import LoginPresentation

type Callback[P: Presentation] = Callable[[P, Any], Awaitable[tuple[P, Any]]]


class RPAClient:
    @dataclass(frozen=True)
    class Config:
        address: str
        port: int

    def __init__(self) -> None:
        self._handlers: dict[
            str,
            Callable[..., Awaitable[tuple[Presentation, Any]]],
        ] = {}

    async def _detect(
        self,
        presentations: frozenset[type[Presentation]],
        driver: browser.DriverBase,
    ) -> Presentation:
        while True:
            for candidate in presentations:
                p = await candidate._detect(driver)  # noqa: SLF001
                if p is not None:
                    return p
            await asyncio.sleep(0.5)

    async def _dispatch(
        self,
        presentation: Presentation,
        data: Any,
    ) -> tuple[Presentation, Any]:
        handler = self._handlers.get(presentation.get_type())
        if handler is None:
            msg = f"no handler registered for {presentation.get_type()}"
            raise RuntimeError(msg)

        await presentation._pre_dispatch()  # noqa: SLF001
        return await handler(presentation, data)

    def on[P: Presentation](
        self,
        presentation_cls: type[P],
    ) -> Callable[[Callback[P]], Callback[P]]:
        def decorator(callback: Callback[P]) -> Callback[P]:
            self._handlers[presentation_cls.get_type()] = callback
            return callback

        return decorator

    async def run(
        self,
        config: Config,
        data: Any,
        detection_timeout: float = 30.0,
        browser_client: browser.ClientBase | None = None,
        browser_driver: browser.DriverBase | None = None,
        presentations: frozenset[type[Presentation]] | None = None,
    ) -> None:
        client = browser_client or browser.Client(config.address, config.port)
        driver = browser_driver or browser.Driver(client)
        ps = presentations or frozenset({LoginPresentation})

        async with client, driver:
            while True:
                async with asyncio.timeout(detection_timeout):
                    p = await self._detect(ps, driver)

                await self._dispatch(p, data)

                if p._is_ended:  # noqa: SLF001
                    break
