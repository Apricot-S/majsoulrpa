import asyncio
from logging import getLogger
from typing import NoReturn, override

from majsoulrpa.assets.templates.room import (
    LEAVE_SETTINGS_PATH,
    LEAVE_TEMPLATE_PATH,
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
    ScreenInvalidArgumentError,
    ScreenStaleError,
)
from majsoulrpa.screens.room.errors import (
    RoomOperation,
    RoomOperationFailureReason,
    RoomOperationRejectedError,
)
from majsoulrpa.screens.room.state import RoomState, RoomStatus
from majsoulrpa.sniffer.events import (
    DecodedRequestResponse,
    DecodedSnifferMessage,
    Direction,
)

ROOM_STATE_INITIALIZATION_TIMEOUT_SECONDS = 5.0
LEAVE_API_NAME = ".lq.Lobby.leaveRoom"

_logger = getLogger(__name__)


class RoomScreen(Screen):
    ROOM_SIGN_TEMPLATE = load_png_template_matcher(
        template_path=ROOM_SIGN_TEMPLATE_PATH,
        settings_path=ROOM_SIGN_SETTINGS_PATH,
    )
    LEAVE_TEMPLATE = load_png_template_matcher(
        template_path=LEAVE_TEMPLATE_PATH,
        settings_path=LEAVE_SETTINGS_PATH,
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
        return self._get_cached_state()

    @_screen_api
    @_requires_active
    async def wait_for_state_change(self, state: RoomState) -> RoomState:
        self_account_id = await self._get_self_account_id()
        await self._drain_room_messages(self_account_id)
        await self._ensure_current_generation()
        current = self._get_cached_state()
        if (
            state.room_id != current.room_id
            or state.self_account_id != current.self_account_id
            or state.version > current.version
            or (state.version == current.version and state != current)
        ):
            screenshot = await self.context.browser.screenshot()
            msg = "state does not belong to the current room snapshot history."
            raise ScreenInvalidArgumentError(msg, screenshot)

        while True:
            current = self._get_cached_state()
            if current.version > state.version:
                if current.status is not RoomStatus.WAITING:
                    self._mark_stale()
                return current

            message = await self._get_sniffer_message()
            await self._apply_room_message(message, self_account_id)
            await self._ensure_current_generation()

    @_screen_api
    @_requires_active
    async def leave(self) -> None:
        self_account_id = await self._get_self_account_id()
        await self._drain_room_messages(self_account_id)
        await self._ensure_current_generation()
        await self._ensure_waiting_state()
        await self.click_template(
            self.LEAVE_TEMPLATE,
            message="leave was not found.",
        )

        while True:
            message = await self._get_sniffer_message()
            await self._apply_room_message(message, self_account_id)
            leave_response = None
            if message.raw.name == LEAVE_API_NAME:
                leave_response = await self._require_leave_response(message)
            await self._ensure_current_generation()
            if (
                leave_response is not None
                and "error" in leave_response.response
            ):
                await self._raise_leave_rejection(leave_response)

            state = self._get_cached_state()
            if state.status is RoomStatus.WAITING:
                continue

            self._mark_stale()
            if (
                message.raw.name == LEAVE_API_NAME
                and state.status is RoomStatus.LEFT
            ):
                return
            screenshot = await self.context.browser.screenshot()
            msg = "Room became inactive while waiting to leave."
            raise ScreenStaleError(msg, screenshot)

    async def _require_leave_response(
        self,
        message: DecodedSnifferMessage,
    ) -> DecodedRequestResponse:
        if (
            isinstance(message, DecodedRequestResponse)
            and message.raw.request_direction is Direction.OUTBOUND
        ):
            return message
        screenshot = await self.context.browser.screenshot()
        msg = "leaveRoom must be an outbound request/response."
        raise ScreenInconsistentMessageError(msg, screenshot)

    async def _raise_leave_rejection(
        self,
        message: DecodedRequestResponse,
    ) -> NoReturn:
        error = message.response["error"]
        if not isinstance(error, dict) or "code" not in error:
            screenshot = await self.context.browser.screenshot()
            msg = "leaveRoom error must be a dict containing code."
            raise ScreenInconsistentMessageError(msg, screenshot)

        code = error["code"]
        if isinstance(code, bool) or not isinstance(code, int):
            screenshot = await self.context.browser.screenshot()
            msg = "leaveRoom error code must be an integer."
            raise ScreenInconsistentMessageError(msg, screenshot)

        _logger.warning("Unrecognized leaveRoom error code: %d.", code)
        screenshot = await self.context.browser.screenshot()
        raise RoomOperationRejectedError(
            RoomOperation.LEAVE,
            RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE,
            code,
            screenshot,
        )

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

    def _get_cached_state(self) -> RoomState:
        state = self.context.room_state_cache.state
        if state is None:
            msg = "Room state is not initialized."
            raise RuntimeError(msg)
        return state

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

    async def _ensure_waiting_state(self) -> None:
        if self._get_cached_state().status is RoomStatus.WAITING:
            return
        screenshot = await self.context.browser.screenshot()
        self._mark_stale()
        msg = "Room is no longer active."
        raise ScreenStaleError(msg, screenshot)

    async def _drain_room_messages(self, self_account_id: int) -> None:
        while (message := self._get_sniffer_message_nowait()) is not None:
            await self._apply_room_message(message, self_account_id)

    async def _apply_room_message(
        self,
        message: DecodedSnifferMessage,
        self_account_id: int,
    ) -> None:
        _logger.info(
            "Sniffer message: %s",
            _format_sniffer_message(message),
        )
        try:
            self.context.room_state_cache.apply(message, self_account_id)
        except Exception as error:
            screenshot = await self.context.browser.screenshot()
            msg = "Room state message is inconsistent."
            raise ScreenInconsistentMessageError(msg, screenshot) from error
