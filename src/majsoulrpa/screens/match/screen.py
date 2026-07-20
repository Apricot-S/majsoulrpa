import asyncio
from logging import getLogger
from typing import NoReturn, assert_never, override

from majsoulrpa.assets.templates.match import (
    SEAT_INDICATOR_SETTINGS_PATH,
    SEAT_INDICATOR_TEMPLATE_PATHS,
)
from majsoulrpa.presentation import Region
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import (
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
    _format_sniffer_message,
    _requires_active,
    _screen_api,
)
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match._action import (
    ACTION_PROTOTYPE_NAME,
    MatchActionDecodeError,
    decode_live_action,
)
from majsoulrpa.screens.match._metadata import (
    AUTH_GAME_NAME,
    MatchMetadata,
    MatchMetadataDecodeError,
    decode_match_metadata,
)
from majsoulrpa.screens.match.event import (
    MatchEvent,
    NewRoundEvent,
    StartMatchEvent,
)
from majsoulrpa.screens.match.state import MatchState
from majsoulrpa.screens.match.store import MatchStateStore
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
)

MATCH_INITIALIZATION_TIMEOUT_SECONDS = 5.0

_DEBUG_MESSAGE_NAMES = frozenset(
    {".lq.Lobby.heatbeat", ".lq.FastTest.checkNetworkDelay"}
)
_WARNING_MESSAGE_NAMES = frozenset(
    {".lq.Lobby.loginBeat", ".lq.Lobby.oauth2Login"}
)

_logger = getLogger(__name__)


class MatchScreen(Screen):
    MOUSE_SAFE_REGION = Region(left=585, top=790, width=1000, height=70)

    SEAT_INDICATOR_TEMPLATES = tuple(
        load_png_template_matcher(
            template_path=template_path,
            settings_path=SEAT_INDICATOR_SETTINGS_PATH,
        )
        for template_path in SEAT_INDICATOR_TEMPLATE_PATHS
    )

    def __init__(self, context: ScreenContext | None = None) -> None:
        super().__init__(context=context)
        self._metadata: MatchMetadata | None = None
        self._start_match_event: StartMatchEvent | None = None
        self._new_round_event: NewRoundEvent | None = None
        self._new_round_has_pending_operation = False
        self._state_store = MatchStateStore()

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls._matches_seat_indicator)

    @override
    async def before_callback(self) -> None:
        await self._move_mouse_away_from_hand()
        timeout = asyncio.timeout(MATCH_INITIALIZATION_TIMEOUT_SECONDS)
        try:
            async with timeout:
                await self._initialize()
        except (MatchActionDecodeError, MatchMetadataDecodeError) as error:
            await self._raise_inconsistent_message(
                "Match state initialization failed.",
                cause=error,
            )
        except TimeoutError as error:
            if not timeout.expired():
                raise
            await self._raise_inconsistent_message(
                "An initial match snapshot did not arrive.",
                cause=error,
            )

    @_screen_api
    @_requires_active
    async def get_state(self) -> MatchState:
        while (message := self._get_sniffer_message_nowait()) is not None:
            try:
                self._apply_initialization_message(message)
            except (MatchActionDecodeError, MatchMetadataDecodeError) as error:
                await self._raise_inconsistent_message(
                    "Match state update failed.",
                    cause=error,
                )
        state = self._state_store.state
        if state is None:
            msg = "MatchScreen has not been initialized."
            raise RuntimeError(msg)
        return state

    async def _initialize(self) -> None:
        while self._state_store.state is None:
            message = await self._get_sniffer_message()
            self._apply_initialization_message(message)

    def _apply_initialization_message(
        self,
        message: DecodedSnifferMessage,
    ) -> None:
        name = message.raw.name
        if name == AUTH_GAME_NAME:
            self._log_initialization_message(message)
            self._apply_auth_game(message)
            self._try_initialize_state()
            return
        if name != ACTION_PROTOTYPE_NAME:
            self._log_initialization_message(message)
            return

        if not isinstance(message, DecodedNotice):
            msg = "ActionPrototype must be a Notice."
            raise MatchActionDecodeError(msg)
        event, decoded_message = decode_live_action(message)
        _logger.info(_format_sniffer_message(decoded_message))
        self._apply_initialization_event(event)
        if isinstance(event, NewRoundEvent):
            self._new_round_has_pending_operation = (
                self._has_pending_operation(decoded_message)
            )
        self._try_initialize_state()

    def _apply_auth_game(self, message: DecodedSnifferMessage) -> None:
        if not isinstance(message, DecodedRequestResponse):
            msg = "authGame must be a request/response."
            raise MatchMetadataDecodeError(msg)
        self_account_id = self.context.account_id
        if self_account_id is None:
            msg = "Match metadata requires a self account ID."
            raise MatchMetadataDecodeError(msg)
        metadata = decode_match_metadata(message, self_account_id)
        if self._metadata is not None and self._metadata != metadata:
            msg = "authGame metadata must not change during initialization."
            raise MatchMetadataDecodeError(msg)
        self._metadata = metadata

    def _try_initialize_state(self) -> None:
        if self._state_store.state is not None:
            return
        if self._metadata is None or self._new_round_event is None:
            return
        try:
            self._state_store.initialize(
                self._metadata,
                self._start_match_event,
                self._new_round_event,
                has_pending_operation=(self._new_round_has_pending_operation),
            )
        except ValueError as error:
            msg = "Initial match state is inconsistent."
            raise MatchMetadataDecodeError(msg) from error

    def _apply_initialization_event(self, event: MatchEvent) -> None:
        match event:
            case StartMatchEvent():
                if self._start_match_event is not None:
                    msg = "ActionMJStart must not be repeated."
                    raise MatchActionDecodeError(msg)
                if self._new_round_event is not None:
                    msg = "ActionMJStart must precede ActionNewRound."
                    raise MatchActionDecodeError(msg)
                self._start_match_event = event
            case NewRoundEvent():
                if self._new_round_event is not None:
                    msg = "ActionNewRound must not be repeated."
                    raise MatchActionDecodeError(msg)
                expected_step = 1 if self._start_match_event is not None else 0
                if event.action_step != expected_step:
                    msg = (
                        "ActionNewRound must be step "
                        f"{expected_step} during match initialization."
                    )
                    raise MatchActionDecodeError(msg)
                self._new_round_event = event
            case _ as unreachable:
                assert_never(unreachable)

    @staticmethod
    def _has_pending_operation(message: DecodedNotice) -> bool:
        data = message.message.get("data")
        if not isinstance(data, dict):
            msg = "Decoded ActionNewRound data must be an object."
            raise MatchActionDecodeError(msg)
        operation = data.get("operation")
        if operation is None:
            return False
        if not isinstance(operation, dict):
            msg = "ActionNewRound operation must be an object."
            raise MatchActionDecodeError(msg)
        operation_list = operation.get("operation_list")
        if not isinstance(operation_list, list):
            msg = "ActionNewRound operation list must be a list."
            raise MatchActionDecodeError(msg)
        return bool(operation_list)

    @staticmethod
    def _log_initialization_message(
        message: DecodedSnifferMessage,
    ) -> None:
        name = message.raw.name
        formatted_message = _format_sniffer_message(message)
        if name in _DEBUG_MESSAGE_NAMES:
            # Heartbeats and network probes are frequent and carry no
            # match state, so keep them out of the information log.
            _logger.debug(formatted_message)
            return
        if name in _WARNING_MESSAGE_NAMES:
            # Login traffic can indicate a reconnect. Make it visible
            # without treating that as a failure.
            _logger.warning(formatted_message)
            return
        _logger.info(formatted_message)

    async def _raise_inconsistent_message(
        self,
        message: str,
        *,
        cause: BaseException,
    ) -> NoReturn:
        screenshot = await self.context.browser.screenshot()
        raise ScreenInconsistentMessageError(message, screenshot) from cause

    async def _move_mouse_away_from_hand(self) -> None:
        # Hovering over a tile in the hand can display winning-tile
        # candidates. They may interfere with template matching, so keep
        # the cursor in the empty area immediately above the hand.
        await self.move_region(self.MOUSE_SAFE_REGION)

    @classmethod
    def _matches_seat_indicator(cls, screenshot: object) -> bool:
        return any(
            template.matches(screenshot)
            for template in cls.SEAT_INDICATOR_TEMPLATES
        )
