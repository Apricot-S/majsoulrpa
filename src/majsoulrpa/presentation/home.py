import asyncio
from typing import ClassVar, Self, override

import majsoulrpa.presentation.templates.home as home_templates
from majsoulrpa import browser, sniffer
from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.base import Presentation


class HomePresentation(Presentation):
    _templates: ClassVar = {
        "summon": home_templates.SUMMON,
    }
    _regions: ClassVar = {}

    @override
    def __init__(
        self,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> None:
        super().__init__(driver, message_queue)

    @override
    @classmethod
    async def _detect(
        cls,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> Self | None:
        p = cls(driver, message_queue)
        await p._init_resolution()
        has_match = await p._has_match(cls._templates["summon"])
        return p if has_match else None

    @override
    async def _pre_dispatch(self) -> None:
        await self._close_notifications()
        await self._drain_message_queue()

        if self._message_queue.account_id is None:
            msg = "Account ID not found after home screen transition."
            raise exceptions.UnexpectedStateError(msg, None)

        await asyncio.sleep(0.5)

    async def _drain_message_queue(self) -> None:
        while self._message_queue.get_nowait() is not None:
            pass

    async def _close_notifications(self) -> None:
        # TODO: 告知の閉じるボタンをクリックする処理を追加する
        pass
