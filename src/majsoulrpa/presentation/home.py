import asyncio
from typing import Self, override

from majsoulrpa import browser
from majsoulrpa.presentation.base import Presentation
from majsoulrpa.presentation.templates.home import SUMMON


class HomePresentation(Presentation):
    @override
    def __init__(self, driver: browser.DriverBase) -> None:
        super().__init__(driver)

    @override
    @classmethod
    async def _detect(cls, driver: browser.DriverBase) -> Self | None:
        p = cls(driver)
        await p._init_resolution()
        has_match = await p._has_match(SUMMON)
        return p if has_match else None

    @override
    async def _pre_dispatch(self) -> None:
        # TODO: イベント画面・告知を消す処理、通信を読み取る処理を実装する
        await asyncio.sleep(0.5)
