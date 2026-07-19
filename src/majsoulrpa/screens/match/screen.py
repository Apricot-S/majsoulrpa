import asyncio
from logging import getLogger
from typing import NoReturn, override

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
)
from majsoulrpa.screens.errors import ScreenInconsistentMessageError
from majsoulrpa.screens.match._action import (
    ACTION_PROTOTYPE_NAME,
    MatchActionDecodeError,
    decode_live_action,
)
from majsoulrpa.screens.match.event import StartMatchEvent  # noqa: TC001
from majsoulrpa.sniffer.events import DecodedNotice, DecodedSnifferMessage

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
        self._start_match_event: StartMatchEvent | None = None

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
                while self._start_match_event is None:
                    message = await self._get_sniffer_message()
                    try:
                        self._apply_initialization_message(message)
                    except MatchActionDecodeError as error:
                        await self._raise_inconsistent_message(
                            "A match action is inconsistent.",
                            cause=error,
                        )
        except TimeoutError as error:
            if not timeout.expired():
                raise
            await self._raise_inconsistent_message(
                "ActionMJStart did not arrive during match initialization.",
                cause=error,
            )

    def _apply_initialization_message(
        self,
        message: DecodedSnifferMessage,
    ) -> None:
        name = message.raw.name
        if name == ACTION_PROTOTYPE_NAME:
            if not isinstance(message, DecodedNotice):
                msg = "ActionPrototype must be a Notice."
                raise MatchActionDecodeError(msg)
            event, decoded_message = decode_live_action(message)
            if event.action_step != 0:
                msg = "ActionMJStart must be step 0."
                raise MatchActionDecodeError(msg)
            _logger.info(_format_sniffer_message(decoded_message))
            self._start_match_event = event
            return

        self._log_initialization_message(message)

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
