import asyncio
from logging import getLogger
from typing import override

from majsoulrpa.assets.templates.room import (
    ROOM_SIGN_SETTINGS_PATH,
    ROOM_SIGN_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import (
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
    _format_sniffer_message,
    _requires_active,
    _screen_api,
)
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
    ScreenStaleError,
)
from majsoulrpa.screens.room.state import RoomState, RoomStatus
from majsoulrpa.sniffer.events import DecodedSnifferMessage

ROOM_STATE_INITIALIZATION_TIMEOUT_SECONDS = 5.0

_logger = getLogger(__name__)


class RoomScreen(Screen):
    ROOM_SIGN_TEMPLATE = load_png_template_matcher(
        template_path=ROOM_SIGN_TEMPLATE_PATH,
        settings_path=ROOM_SIGN_SETTINGS_PATH,
    )

    def __init__(self, context: ScreenContext | None = None) -> None:
        super().__init__(context=context)
        self._room_generation: int | None = None

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls.ROOM_SIGN_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        self_account_id = await self._get_self_account_id()
        await self._drain_room_messages(self_account_id)
        timeout = asyncio.timeout(
            ROOM_STATE_INITIALIZATION_TIMEOUT_SECONDS,
        )
        try:
            async with timeout:
                while not self._has_active_room_state():
                    message = await self._get_sniffer_message()
                    await self._apply_room_message(message, self_account_id)
        except TimeoutError as error:
            if not timeout.expired():
                raise
            screenshot = await self.context.browser.screenshot()
            msg = "An active room snapshot did not arrive."
            raise ScreenInconsistentMessageError(msg, screenshot) from error
        self._room_generation = self.context.room_state_cache.generation

    @_screen_api
    @_requires_active
    async def get_state(self) -> RoomState:
        await self._drain_room_messages(await self._get_self_account_id())
        await self._ensure_current_generation()
        state = self.context.room_state_cache.state
        if state is None:
            msg = "Room state is not initialized."
            raise RuntimeError(msg)
        return state

    async def _get_self_account_id(self) -> int:
        self_account_id = self.context.account_id
        if self_account_id is None:
            screenshot = await self.context.browser.screenshot()
            msg = "Room state requires a self account ID."
            raise ScreenInconsistentMessageError(msg, screenshot)
        return self_account_id

    def _has_active_room_state(self) -> bool:
        state = self.context.room_state_cache.state
        return state is not None and state.status is RoomStatus.WAITING

    async def _ensure_current_generation(self) -> None:
        if self._room_generation is None:
            msg = "RoomScreen has not been initialized."
            raise RuntimeError(msg)
        if self._room_generation == self.context.room_state_cache.generation:
            return

        screenshot = await self.context.browser.screenshot()
        self._mark_stale()
        msg = "RoomScreen belongs to an old room generation."
        raise ScreenStaleError(msg, screenshot)

    async def _drain_room_messages(self, self_account_id: int) -> None:
        while (message := self._get_sniffer_message_nowait()) is not None:
            await self._apply_room_message(message, self_account_id)

    async def _apply_room_message(
        self,
        message: DecodedSnifferMessage,
        self_account_id: int,
    ) -> None:
        try:
            self.context.room_state_cache.apply(message, self_account_id)
        except Exception as error:
            screenshot = await self.context.browser.screenshot()
            msg = "Room state message is inconsistent."
            raise ScreenInconsistentMessageError(msg, screenshot) from error
        _logger.info(
            "Sniffer message: %s",
            _format_sniffer_message(message),
        )
