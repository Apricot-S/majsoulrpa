import asyncio
from typing import TYPE_CHECKING, ClassVar, Self, override

import majsoulrpa.presentation.templates.home as home_templates
from majsoulrpa import browser, sniffer
from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.base import Presentation, require_active
from majsoulrpa.presentation.room_settings import Length, Mode, ThinkingTime

if TYPE_CHECKING:
    from majsoulrpa.sniffer.message import Message


class HomePresentation(Presentation):
    _templates: ClassVar = {
        "summon": home_templates.SUMMON,
        "jade": home_templates.JADE,
        "notification_close": home_templates.NOTIFICATION_CLOSE,
        "mail_close": home_templates.MAIL_CLOSE,
        "event_close": home_templates.EVENT_CLOSE,
        "rewards_sign_in": home_templates.REWARDS_SIGN_IN,
        "rewards_confirm": home_templates.REWARDS_CONFIRM,
        "friendly_match": home_templates.FRIENDLY_MATCH,
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
        if self._has_month_ticket():
            await self._receive_daily_bonus()

        await asyncio.sleep(0.5)
        await self._close_notifications()

        if not await self._ensure_home_screen_ready():
            msg = "Home screen did not become interactable."
            ss = await self.get_screenshot()
            raise exceptions.UnexpectedStateError(msg, ss)

        self._drain_message_queue()
        if self._message_queue.account_id is None:
            msg = "Account ID not found after home screen transition."
            raise exceptions.UnexpectedStateError(msg, None)

    def _has_month_ticket(self) -> bool:
        buffer: list[Message] = []
        has_ticket = False

        while (message := self._message_queue.get_nowait()) is not None:
            buffer.append(message)
            if message.name == ".lq.Lobby.payMonthTicket":
                has_ticket = True
                break

        for m in buffer:
            self._message_queue.put_back(m)

        return has_ticket

    async def _receive_daily_bonus(self) -> None:
        try:
            async with asyncio.timeout(5):
                await self._click_when_match(self._templates["jade"])
        except TimeoutError as e:
            msg = "Daily bonus jade was not detected."
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss) from e

        await asyncio.sleep(0.5)

    async def _close_notifications(self) -> None:
        while await self._close_notifications_impl():
            pass

    async def _close_notifications_impl(self) -> bool:
        templates = [
            self._templates["notification_close"],
            self._templates["mail_close"],
            self._templates["event_close"],
        ]
        if await self._click_if_match_one_of(templates):
            await asyncio.sleep(1.0)
            return True

        if await self._click_if_match(self._templates["rewards_sign_in"]):
            await asyncio.sleep(2.0)

            if await self._click_if_match(self._templates["rewards_confirm"]):
                await asyncio.sleep(0.5)
                return True

            msg = '"Confirm" button for accumulated sign in rewards could not be detected.'  # noqa: E501
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        return False

    async def _ensure_home_screen_ready(self) -> bool:
        return await self._has_match(self._templates["friendly_match"])

    def _drain_message_queue(self) -> None:
        while self._message_queue.get_nowait() is not None:
            pass

    @require_active
    async def create_room(
        self,
        mode: Mode = Mode.FOUR_PLAYER,
        length: Length = Length.TWO_WIND_MATCH,
        thinking_time: ThinkingTime = ThinkingTime.FivePlusTwenty,
    ) -> None:
        if not await self._click_if_match(self._templates["friendly_match"]):
            msg = '"Friendly Match" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        raise NotImplementedError
