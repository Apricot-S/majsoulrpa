import asyncio
import re
from enum import Enum
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar, Self, assert_never, override

import majsoulrpa.presentation.regions.home as home_regions
import majsoulrpa.presentation.templates.home as home_templates
from majsoulrpa import browser, sniffer
from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.base import Presentation, rpa_api
from majsoulrpa.presentation.room_settings import Length, Mode, ThinkingTime

if TYPE_CHECKING:
    from majsoulrpa.sniffer.message import Message

logger = getLogger(__name__)

ROOM_ID_PATTERN = re.compile(r"\d{5}")


class JoinRoomFailureReason(Enum):
    """Reason for failure to join a friendly match room.

    Attributes:
        NOT_FOUND: The room was not found.
        FULL: The room was full.
        ALREADY_STARTED: A match was already started.
        UNKNOWN: An unrecognized or unsupported error code.
    """

    NOT_FOUND = 1100
    FULL = 1101
    ALREADY_STARTED = 1109
    UNKNOWN = -1


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
        "create_room": home_templates.CREATE_ROOM,
        "create_room/create": home_templates.create_room.CREATE,
        "create_room/4-player": home_templates.create_room.FOUR_PLAYER,
        "create_room/3-player": home_templates.create_room.THREE_PLAYER,
        "create_room/1_game": home_templates.create_room.ONE_GAME,
        "create_room/east_only": home_templates.create_room.EAST_ONLY,
        "create_room/two-wind_match": home_templates.create_room.TWO_WIND_MATCH,  # noqa: E501
        "create_room/vs_ai": home_templates.create_room.VS_AI,
        "create_room/3+5s": home_templates.create_room.THREE_PLUS_FIVE,
        "create_room/5+10s": home_templates.create_room.FIVE_PLUS_TEN,
        "create_room/5+20s": home_templates.create_room.FIVE_PLUS_TWENTY,
        "create_room/60+0s": home_templates.create_room.SIXTY_PLUS_ZERO,
        "create_room/300+0s": home_templates.create_room.THREE_HUNDRED_PLUS_ZERO,  # noqa: E501
        "join_room": home_templates.JOIN_ROOM,
        "join_room/confirm": home_templates.join_room.CONFIRM,
    }
    _regions: ClassVar = {
        "join_room/room_id_field": home_regions.join_room.ROOM_ID_FIELD,
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

    @rpa_api
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

        await asyncio.sleep(1.0)

        if not await self._click_if_match(self._templates["create_room"]):
            msg = '"Create Room" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        await asyncio.sleep(1.0)

        if not await self._has_match(self._templates["create_room/create"]):
            msg = '"Create" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        match mode:
            case Mode.FOUR_PLAYER:
                mode_template = self._templates["create_room/4-player"]
            case Mode.THREE_PLAYER:
                mode_template = self._templates["create_room/3-player"]
            case _ as unreachable_mode:
                assert_never(unreachable_mode)

        match length:
            case Length.ONE_GAME:
                length_template = self._templates["create_room/1_game"]
            case Length.EAST_ONLY:
                length_template = self._templates["create_room/east_only"]
            case Length.TWO_WIND_MATCH:
                length_template = self._templates["create_room/two-wind_match"]
            case Length.VS_AI:
                length_template = self._templates["create_room/vs_ai"]
            case _ as unreachable_length:
                assert_never(unreachable_length)

        match thinking_time:
            case ThinkingTime.ThreePlusFive:
                thinking_time_template = self._templates["create_room/3+5s"]
            case ThinkingTime.FivePlusTen:
                thinking_time_template = self._templates["create_room/5+10s"]
            case ThinkingTime.FivePlusTwenty:
                thinking_time_template = self._templates["create_room/5+20s"]
            case ThinkingTime.SixtyPlusZero:
                thinking_time_template = self._templates["create_room/60+0s"]
            case ThinkingTime.ThreeHundredPlusZero:
                thinking_time_template = self._templates["create_room/300+0s"]
            case _ as unreachable_thinking_time:
                assert_never(unreachable_thinking_time)

        # No need to click if already selected
        await self._click_if_match(mode_template)
        await asyncio.sleep(0.5)
        await self._click_if_match(length_template)
        await asyncio.sleep(0.5)
        await self._click_if_match(thinking_time_template)
        await asyncio.sleep(0.5)

        if not await self._click_if_match(
            self._templates["create_room/create"],
        ):
            msg = '"Create" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        self._mark_finished()

    @rpa_api
    async def join_room(self, room_id: str) -> JoinRoomFailureReason | None:
        if ROOM_ID_PATTERN.fullmatch(room_id) is None:
            msg = "Room ID must be a 5-digit number."
            raise exceptions.InvalidArgumentError(msg, None)

        if not await self._click_if_match(self._templates["friendly_match"]):
            msg = '"Friendly Match" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        await asyncio.sleep(1.0)

        if not await self._click_if_match(self._templates["join_room"]):
            msg = '"Join Room" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        await asyncio.sleep(1.0)

        if not await self._has_match(self._templates["join_room/confirm"]):
            msg = '"Confirm" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        # Click the text box to focus it.
        await self._click_region(self._regions["join_room/room_id_field"])
        await asyncio.sleep(0.5)

        # Enter the room ID in the text box.
        await self._type_key(room_id)
        await asyncio.sleep(0.5)

        if not await self._click_if_match(
            self._templates["join_room/confirm"],
        ):
            msg = '"Confirm" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        # Wait for `.lq.Lobby.joinRoom` to be exchanged.
        await asyncio.sleep(0.5)

        join_room_message = None
        while (message := self._message_queue.get_nowait()) is not None:
            if message.name == ".lq.Lobby.joinRoom":
                join_room_message = message
                break

        if join_room_message is None:
            msg = "`.lq.Lobby.joinRoom` was not exchanged."
            ss = await self.get_screenshot()
            raise exceptions.InconsistentMessageError(msg, ss)

        response = join_room_message.response
        if response is None:
            msg = "`.lq.Lobby.joinRoom` has no response message."
            raise exceptions.InconsistentMessageError(msg, None)

        failure_reason = self._parse_error_code(response)
        if failure_reason is None:
            logger.info("Successfully joined room.")
            self._mark_finished()
            return None

        logger.warning("Failed to join room. reason=%s", failure_reason.name)

        await asyncio.sleep(0.5)
        if not await self._click_if_match(
            self._templates["join_room/error_confirm"],
        ):
            msg = '"Confirm" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        return failure_reason

    @staticmethod
    def _parse_error_code(
        response: dict[str, Any],
    ) -> JoinRoomFailureReason | None:
        error: dict | None = response.get("error")
        if error is None:
            return None

        error_code = error.get("code")
        if error_code is None:
            msg = f"No error code in `.lq.Lobby.joinRoom`. {response=}"
            raise exceptions.InconsistentMessageError(msg, None)

        try:
            return JoinRoomFailureReason(error_code)
        except ValueError:
            logger.exception(
                "Unsupported error code in `.lq.Lobby.joinRoom`. Falling back to UNKNOWN. response=%s",  # noqa: E501
                response,
            )
            return JoinRoomFailureReason.UNKNOWN
