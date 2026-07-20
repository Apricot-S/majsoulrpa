import asyncio
from logging import getLogger
from typing import NoReturn, override

from majsoulrpa.assets.templates.room import (
    ADD_AI_SETTINGS_PATHS,
    ADD_AI_TEMPLATE_PATH,
    CANCEL_SETTINGS_PATH,
    CANCEL_TEMPLATE_PATH,
    LEAVE_SETTINGS_PATH,
    LEAVE_TEMPLATE_PATH,
    READY_SETTINGS_PATH,
    READY_TEMPLATE_PATH,
    ROOM_SIGN_SETTINGS_PATH,
    ROOM_SIGN_TEMPLATE_PATH,
    START_SETTINGS_PATH,
    START_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import (
    TEMPLATE_DETECTION_RETRY_INTERVAL_SECONDS,
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
    _format_sniffer_message_for_log,
    _requires_active,
    _screen_api,
)
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenStaleError,
)
from majsoulrpa.screens.room.errors import (
    RoomOperation,
    RoomOperationFailureReason,
    RoomOperationNotAllowedError,
    RoomOperationNotAllowedReason,
    RoomOperationRejectedError,
)
from majsoulrpa.screens.room.state import RoomState, RoomStatus
from majsoulrpa.screens.room.store import RoomStateStore
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
    Direction,
)

ROOM_STATE_INITIALIZATION_TIMEOUT_SECONDS = 5.0
LEAVE_API_NAME = ".lq.Lobby.leaveRoom"
ADD_AI_API_NAME = ".lq.Lobby.addRoomRobot"
PLAYER_UPDATE_NOTICE_NAME = ".lq.NotifyRoomPlayerUpdate"
START_MATCH_API_NAME = ".lq.Lobby.startRoom"
GAME_START_NOTICE_NAME = ".lq.NotifyRoomGameStart"
SET_READY_API_NAME = ".lq.Lobby.readyPlay"
PLAYER_READY_NOTICE_NAME = ".lq.NotifyRoomPlayerReady"

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
    ADD_AI_TEMPLATES = tuple(
        load_png_template_matcher(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=settings_path,
        )
        for settings_path in ADD_AI_SETTINGS_PATHS
    )
    START_MATCH_TEMPLATE = load_png_template_matcher(
        template_path=START_TEMPLATE_PATH,
        settings_path=START_SETTINGS_PATH,
    )
    READY_TEMPLATE = load_png_template_matcher(
        template_path=READY_TEMPLATE_PATH,
        settings_path=READY_SETTINGS_PATH,
    )
    CANCEL_TEMPLATE = load_png_template_matcher(
        template_path=CANCEL_TEMPLATE_PATH,
        settings_path=CANCEL_SETTINGS_PATH,
    )

    def __init__(self, context: ScreenContext | None = None) -> None:
        super().__init__(context=context)
        self._room_state_store = RoomStateStore()
        self._room_state_initialized = False

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
        self._room_state_initialized = True

    @_screen_api
    @_requires_active
    async def get_state(self) -> RoomState:
        await self._drain_room_messages(await self._get_self_account_id())
        await self._ensure_room_state_initialized()
        return self._get_room_state()

    @_screen_api
    @_requires_active
    async def wait_for_state_change(self, state: RoomState) -> RoomState:
        self_account_id = await self._get_self_account_id()
        await self._drain_room_messages(self_account_id)
        await self._ensure_room_state_initialized()
        current = self._get_room_state()
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
            current = self._get_room_state()
            if current.version > state.version:
                if current.status is RoomStatus.MATCH_STARTED:
                    try:
                        await self._wait_until_room_disappears()
                    finally:
                        self._mark_stale()
                elif current.status is not RoomStatus.WAITING:
                    self._mark_stale()
                return current

            message = await self._get_sniffer_message()
            await self._apply_room_message(message, self_account_id)
            await self._ensure_room_state_initialized()

    @_screen_api
    @_requires_active
    async def leave(self) -> None:
        self_account_id, _ = await self._prepare_room_operation()
        await self.click_template(
            self.LEAVE_TEMPLATE,
            message="leave was not found.",
        )

        while True:
            message = await self._get_sniffer_message()
            await self._apply_room_message(message, self_account_id)
            await self._ensure_room_state_initialized()
            state = self._get_room_state()

            if message.raw.name == LEAVE_API_NAME:
                response = await self._require_operation_response(message)
                if "error" in response.response:
                    await self._raise_operation_rejection(
                        response,
                        RoomOperation.LEAVE,
                    )
                if state.status is RoomStatus.LEFT:
                    self._mark_stale()
                    await asyncio.sleep(1.0)
                    return

            if state.status is RoomStatus.WAITING:
                continue

            self._mark_stale()
            screenshot = await self.context.browser.screenshot()
            msg = "Room became inactive while waiting to leave."
            raise ScreenStaleError(msg, screenshot)

    @_screen_api
    @_requires_active
    async def add_ai(self) -> RoomState:
        self_account_id, previous = await self._prepare_room_operation()
        await self._ensure_add_ai_allowed(previous)
        await self._click_add_ai_template()

        expected_ai_count = previous.ai_count + 1
        response_succeeded = False
        ai_update_succeeded = False
        state = previous
        while not (
            response_succeeded
            and ai_update_succeeded
            and state.ai_count == expected_ai_count
        ):
            message = await self._get_sniffer_message()
            await self._apply_room_message(message, self_account_id)
            await self._ensure_room_state_initialized()
            await self._ensure_waiting_state()
            state = self._get_room_state()

            if message.raw.name == ADD_AI_API_NAME:
                response = await self._require_operation_response(message)
                if "error" in response.response:
                    await self._raise_operation_rejection(
                        response,
                        RoomOperation.ADD_AI,
                    )
                response_succeeded = True
            elif message.raw.name == PLAYER_UPDATE_NOTICE_NAME:
                ai_update_succeeded = state.ai_count == expected_ai_count

        return state

    @_screen_api
    @_requires_active
    async def start_match(self) -> None:
        self_account_id, state = await self._prepare_room_operation()
        await self._ensure_start_match_allowed(state)
        await self.click_template(
            self.START_MATCH_TEMPLATE,
            message="start was not found.",
        )

        response_succeeded = False
        game_start_succeeded = False
        try:
            while not (response_succeeded and game_start_succeeded):
                message = await self._get_sniffer_message()
                await self._apply_room_message(message, self_account_id)
                await self._ensure_room_state_initialized()
                state = self._get_room_state()

                if message.raw.name == START_MATCH_API_NAME:
                    response = await self._require_operation_response(message)
                    if "error" in response.response:
                        await self._raise_operation_rejection(
                            response,
                            RoomOperation.START_MATCH,
                        )
                    response_succeeded = True
                elif message.raw.name == GAME_START_NOTICE_NAME:
                    game_start_succeeded = (
                        state.status is RoomStatus.MATCH_STARTED
                    )

                if state.status in {
                    RoomStatus.WAITING,
                    RoomStatus.MATCH_STARTED,
                }:
                    continue

                self._mark_stale()
                screenshot = await self.context.browser.screenshot()
                msg = "Room became inactive while waiting to start the match."
                raise ScreenStaleError(msg, screenshot)

            await self._wait_until_room_disappears()
        finally:
            if game_start_succeeded:
                self._mark_stale()

    @_screen_api
    @_requires_active
    async def set_ready(self, *, ready: bool = True) -> RoomState:
        self_account_id, previous = await self._prepare_room_operation()
        await self._ensure_set_ready_allowed(previous)
        if previous.self_is_ready is ready:
            return previous

        template = self.READY_TEMPLATE if ready else self.CANCEL_TEMPLATE
        await self.click_template(
            template,
            message=f"{'ready' if ready else 'cancel'} was not found.",
        )

        response_succeeded = False
        ready_update_succeeded = False
        state = previous
        while not (
            response_succeeded
            and ready_update_succeeded
            and state.self_is_ready is ready
        ):
            message = await self._get_sniffer_message()
            await self._apply_room_message(message, self_account_id)
            await self._ensure_room_state_initialized()
            await self._ensure_waiting_state()
            state = self._get_room_state()

            if message.raw.name == SET_READY_API_NAME:
                response = await self._require_operation_response(message)
                if response.request.get("ready") is not ready:
                    screenshot = await self.context.browser.screenshot()
                    msg = "readyPlay request does not match the target state."
                    raise ScreenInconsistentMessageError(msg, screenshot)
                if "error" in response.response:
                    await self._raise_operation_rejection(
                        response,
                        RoomOperation.SET_READY,
                    )
                response_succeeded = True
            elif message.raw.name == PLAYER_READY_NOTICE_NAME:
                ready_update_succeeded = (
                    ready_update_succeeded
                    or self._is_self_ready_notice(
                        message,
                        self_account_id,
                        ready=ready,
                    )
                )

        return state

    async def _prepare_room_operation(self) -> tuple[int, RoomState]:
        self_account_id = await self._get_self_account_id()
        await self._drain_room_messages(self_account_id)
        await self._ensure_room_state_initialized()
        await self._ensure_waiting_state()
        return self_account_id, self._get_room_state()

    async def _require_operation_response(
        self,
        message: DecodedSnifferMessage,
    ) -> DecodedRequestResponse:
        if (
            isinstance(message, DecodedRequestResponse)
            and message.raw.request_direction is Direction.OUTBOUND
        ):
            return message
        screenshot = await self.context.browser.screenshot()
        operation_name = message.raw.name.rsplit(".", maxsplit=1)[-1]
        msg = f"{operation_name} must be an outbound request/response."
        raise ScreenInconsistentMessageError(msg, screenshot)

    async def _raise_operation_rejection(
        self,
        message: DecodedRequestResponse,
        operation: RoomOperation,
    ) -> NoReturn:
        error = message.response["error"]
        operation_name = message.raw.name.rsplit(".", maxsplit=1)[-1]
        if not isinstance(error, dict) or "code" not in error:
            screenshot = await self.context.browser.screenshot()
            msg = f"{operation_name} error must be a dict containing code."
            raise ScreenInconsistentMessageError(msg, screenshot)

        code = error["code"]
        if isinstance(code, bool) or not isinstance(code, int):
            screenshot = await self.context.browser.screenshot()
            msg = f"{operation_name} error code must be an integer."
            raise ScreenInconsistentMessageError(msg, screenshot)

        _logger.warning(
            "Unrecognized %s error code: %d.",
            operation_name,
            code,
        )
        screenshot = await self.context.browser.screenshot()
        raise RoomOperationRejectedError(
            operation,
            RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE,
            code,
            screenshot,
        )

    async def _ensure_add_ai_allowed(self, state: RoomState) -> None:
        reason = None
        if not state.self_is_host:
            reason = RoomOperationNotAllowedReason.NOT_HOST
        elif state.available_slots == 0:
            reason = RoomOperationNotAllowedReason.ROOM_FULL
        if reason is None:
            return

        screenshot = await self.context.browser.screenshot()
        raise RoomOperationNotAllowedError(
            RoomOperation.ADD_AI,
            reason,
            screenshot,
        )

    async def _ensure_start_match_allowed(self, state: RoomState) -> None:
        reason = None
        if not state.self_is_host:
            reason = RoomOperationNotAllowedReason.NOT_HOST
        elif state.available_slots != 0:
            reason = RoomOperationNotAllowedReason.ROOM_NOT_FULL
        elif not state.all_guests_ready:
            reason = RoomOperationNotAllowedReason.GUEST_NOT_READY
        if reason is None:
            return

        screenshot = await self.context.browser.screenshot()
        raise RoomOperationNotAllowedError(
            RoomOperation.START_MATCH,
            reason,
            screenshot,
        )

    async def _ensure_set_ready_allowed(self, state: RoomState) -> None:
        if not state.self_is_host:
            return

        screenshot = await self.context.browser.screenshot()
        raise RoomOperationNotAllowedError(
            RoomOperation.SET_READY,
            RoomOperationNotAllowedReason.NOT_GUEST,
            screenshot,
        )

    @staticmethod
    def _is_self_ready_notice(
        message: DecodedSnifferMessage,
        self_account_id: int,
        *,
        ready: bool,
    ) -> bool:
        return (
            isinstance(message, DecodedNotice)
            and message.message.get("account_id") == self_account_id
            and message.message.get("ready") is ready
        )

    async def _click_add_ai_template(self) -> None:
        screenshot = await self.context.browser.screenshot()
        for template in self.ADD_AI_TEMPLATES:
            result = template.find(screenshot)
            if result is None:
                continue
            await self._click_region(result.region)
            return

        msg = "add-ai was not found."
        raise ScreenDetectionError(msg, screenshot)

    async def _wait_until_room_disappears(self) -> None:
        while True:
            screenshot = await self.context.browser.screenshot()
            if not self.ROOM_SIGN_TEMPLATE.matches(screenshot):
                return
            await asyncio.sleep(TEMPLATE_DETECTION_RETRY_INTERVAL_SECONDS)

    async def _get_self_account_id(self) -> int:
        self_account_id = self.context.account_id
        if self_account_id is None:
            screenshot = await self.context.browser.screenshot()
            msg = "Room state requires a self account ID."
            raise ScreenInconsistentMessageError(msg, screenshot)
        return self_account_id

    def _has_active_room_state(self) -> bool:
        state = self._room_state_store.state
        return state is not None and state.status is RoomStatus.WAITING

    def _get_room_state(self) -> RoomState:
        state = self._room_state_store.state
        if state is None:
            msg = "Room state is not initialized."
            raise RuntimeError(msg)
        return state

    async def _ensure_room_state_initialized(self) -> None:
        if not self._room_state_initialized:
            msg = "RoomScreen has not been initialized."
            raise RuntimeError(msg)

    async def _ensure_waiting_state(self) -> None:
        if self._get_room_state().status is RoomStatus.WAITING:
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
        _logger.info(_format_sniffer_message_for_log(message))
        try:
            self._room_state_store.apply(message, self_account_id)
        except Exception as error:
            screenshot = await self.context.browser.screenshot()
            msg = "Room state message is inconsistent."
            raise ScreenInconsistentMessageError(msg, screenshot) from error
