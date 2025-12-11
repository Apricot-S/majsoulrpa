import asyncio
from typing import ClassVar, Self, override

import majsoulrpa.presentation.templates.home as home_templates
from majsoulrpa import browser, sniffer
from majsoulrpa.presentation.base import Presentation


class HomePresentation(Presentation):
    _templates: ClassVar = {
        "summon": home_templates.SUMMON,
    }

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
        # TODO: イベント画面・告知を消す処理、通信を読み取る処理を実装する
        await asyncio.sleep(0.5)
