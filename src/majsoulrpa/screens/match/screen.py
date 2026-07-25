import asyncio
from logging import getLogger
from typing import TYPE_CHECKING, NoReturn, assert_never, override

from majsoulrpa._clock import utc_now
from majsoulrpa.assets.templates.match import (
    BABEI_TEMPLATE_PATH,
    BUTTON_AREA_SETTINGS_PATH,
    CHI_TEMPLATE_PATH,
    GANG_TEMPLATE_PATH,
    LIQI_TEMPLATE_PATH,
    LIUJU_TEMPLATE_PATH,
    PENG_TEMPLATE_PATH,
    SEAT_INDICATOR_SETTINGS_PATH,
    SEAT_INDICATOR_TEMPLATE_PATHS,
)
from majsoulrpa.presentation import Region
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import (
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
    TemplateMatcher,
    _format_sniffer_message_for_log,
    _requires_active,
    _screen_api,
)
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenInvalidOperationError,
    ScreenNotImplementedOperationError,
    ScreenUnexpectedStateError,
)
from majsoulrpa.screens.match._action import (
    ACTION_PROTOTYPE_NAME,
    MatchActionDecodeError,
    decode_live_action,
)
from majsoulrpa.screens.match._common import normalize_tile_kind
from majsoulrpa.screens.match._metadata import (
    AUTH_GAME_NAME,
    MatchMetadata,
    MatchMetadataDecodeError,
    MatchMetadataUnsupportedError,
    decode_match_metadata,
)
from majsoulrpa.screens.match.event import (
    AngangEvent,
    BabeiEvent,
    ChiEvent,
    DaminggangEvent,
    DapaiEvent,
    HuleEvent,
    JiagangEvent,
    LiujuEvent,
    LiujuType,
    MatchEvent,
    NewRoundEvent,
    PengEvent,
    StartMatchEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation import (
    AngangOperation,
    BabeiOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    JiagangOperation,
    LiqiOperation,
    LiujuOperation,
    MatchOperation,
    PengOperation,
    RongOperation,
    ZimohuOperation,
)
from majsoulrpa.screens.match.operation._specification import (
    _OperationCandidatesSpecification,
)
from majsoulrpa.screens.match.state import MatchState
from majsoulrpa.screens.match.store import MatchStateStore
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
)

if TYPE_CHECKING:
    import datetime

MATCH_INITIALIZATION_TIMEOUT_SECONDS = 5.0
DEALER_FIRST_DISCARD_DELAY_SECONDS = 2.0
DAPAI_UI_READY_DELAY_SECONDS = 0.4
DAPAI_CLICK_RETRY_INTERVAL_SECONDS = 0.5
OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS = 0.5
OPERATION_OPTION_DISPLAY_DELAY_SECONDS = 0.4
HAND_SLIDE_DELAY_SECONDS = 1.5

_SINGLE_FULU_CANDIDATE_COUNT = 1
_MIN_MULTIPLE_FULU_CANDIDATE_COUNT = 2
_MAX_CHI_CANDIDATE_COUNT = 5
_MAX_PENG_CANDIDATE_COUNT = 2
_MAX_ANGANG_JIAGANG_CANDIDATE_COUNT = 3

_DAPAI_CLICK_PROGRESS_MESSAGE_NAMES = frozenset(
    {
        ".lq.FastTest.inputOperation",
        ".lq.FastTest.inputChiPengGang",
        ACTION_PROTOTYPE_NAME,
    }
)

_DEBUG_MESSAGE_NAMES = frozenset(
    {".lq.Lobby.heatbeat", ".lq.FastTest.checkNetworkDelay"}
)
_WARNING_MESSAGE_NAMES = frozenset(
    {".lq.Lobby.loginBeat", ".lq.Lobby.oauth2Login"}
)

_logger = getLogger(__name__)


class MatchScreen(Screen):
    MOUSE_SAFE_REGION = Region(left=585, top=790, width=1000, height=70)
    HAND_TILE_REGION = Region(left=232, top=936, width=71, height=104)
    HAND_TILE_HORIZONTAL_INTERVAL = 94.91
    ZIMOPAI_REGIONS = (
        Region(left=356, top=936, width=71, height=104),
        Region(left=641, top=936, width=71, height=104),
        Region(left=926, top=936, width=71, height=104),
        Region(left=1211, top=936, width=71, height=104),
        Region(left=1495, top=936, width=71, height=104),
    )
    CHI_PENG_COMBINATION_REGION = Region(
        left=961,
        top=692,
        width=157,
        height=117,
    )
    CHI_PENG_COMBINATION_HORIZONTAL_INTERVAL = 200
    CHI_PENG_COMBINATION_CENTERING_INTERVAL = 100
    ANGANG_JIAGANG_TWO_CANDIDATE_REGIONS = (
        Region(left=601, top=692, width=317, height=117),
        Region(left=961, top=692, width=317, height=117),
    )
    AUTO_HULE_TOGGLE_YONMA_REGION = Region(
        left=18,
        top=590,
        width=42,
        height=42,
    )
    AUTO_HULE_TOGGLE_SANMA_REGION = Region(
        left=18,
        top=558,
        width=42,
        height=42,
    )

    SEAT_INDICATOR_TEMPLATES = tuple(
        load_png_template_matcher(
            template_path=template_path,
            settings_path=SEAT_INDICATOR_SETTINGS_PATH,
        )
        for template_path in SEAT_INDICATOR_TEMPLATE_PATHS
    )
    CHI_BUTTON_TEMPLATE = load_png_template_matcher(
        template_path=CHI_TEMPLATE_PATH,
        settings_path=BUTTON_AREA_SETTINGS_PATH,
    )
    PENG_BUTTON_TEMPLATE = load_png_template_matcher(
        template_path=PENG_TEMPLATE_PATH,
        settings_path=BUTTON_AREA_SETTINGS_PATH,
    )
    GANG_BUTTON_TEMPLATE = load_png_template_matcher(
        template_path=GANG_TEMPLATE_PATH,
        settings_path=BUTTON_AREA_SETTINGS_PATH,
    )
    LIQI_BUTTON_TEMPLATE = load_png_template_matcher(
        template_path=LIQI_TEMPLATE_PATH,
        settings_path=BUTTON_AREA_SETTINGS_PATH,
    )
    LIUJU_BUTTON_TEMPLATE = load_png_template_matcher(
        template_path=LIUJU_TEMPLATE_PATH,
        settings_path=BUTTON_AREA_SETTINGS_PATH,
    )
    BABEI_BUTTON_TEMPLATE = load_png_template_matcher(
        template_path=BABEI_TEMPLATE_PATH,
        settings_path=BUTTON_AREA_SETTINGS_PATH,
    )

    def __init__(self, context: ScreenContext | None = None) -> None:
        super().__init__(context=context)
        self._metadata: MatchMetadata | None = None
        self._start_match_event: StartMatchEvent | None = None
        self._new_round_event: NewRoundEvent | None = None
        self._new_round_operation_specification: (
            _OperationCandidatesSpecification | None
        ) = None
        self._operation_candidates_observed_at: datetime.datetime | None = None
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
        except MatchMetadataUnsupportedError as error:
            await self._raise_unsupported_match(cause=error)
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
            await self._apply_match_message_with_screen_errors(
                message,
                inconsistent_message="Match state update failed.",
            )
        state = self._state_store.state
        if state is None:
            msg = "MatchScreen has not been initialized."
            raise RuntimeError(msg)
        return state

    @_screen_api
    @_requires_active
    async def operate(self, operation: MatchOperation) -> MatchState:
        state = await self.get_state()
        candidates = state.round.operation_candidates
        if candidates is None:
            screenshot = await self.context.browser.screenshot()
            msg = "No operation is currently available."
            raise ScreenInvalidOperationError(msg, screenshot)
        if operation not in candidates.operations:
            screenshot = await self.context.browser.screenshot()
            msg = "operation is not one of the current candidates."
            raise ScreenInvalidArgumentError(msg, screenshot)

        match operation:
            case DapaiOperation():
                await self._operate_dapai(state, operation)
            case ChiOperation():
                await self._operate_chi(state, operation)
            case PengOperation():
                await self._operate_peng(state, operation)
            case AngangOperation():
                await self._operate_angang(state, operation)
            case DaminggangOperation():
                await self._operate_daminggang(state, operation)
            case JiagangOperation():
                await self._operate_jiagang(state, operation)
            case LiqiOperation():
                await self._operate_liqi(state, operation)
            case ZimohuOperation():
                await self._operate_zimohu(state, operation)
            case RongOperation():
                await self._operate_rong(state, operation)
            case LiujuOperation():
                await self._operate_liuju(state, operation)
            case BabeiOperation():
                await self._operate_babei(state, operation)
            case _ as unreachable:
                assert_never(unreachable)

        previous_version = state.version
        while True:
            message = await self._get_sniffer_message()
            await self._apply_match_message_with_screen_errors(
                message,
                inconsistent_message=(
                    "Match state update failed while operating."
                ),
            )

            current = self._state_store.state
            if current is None:
                msg = "MatchScreen has not been initialized."
                raise RuntimeError(msg)
            if current.version == previous_version:
                continue

            event = current.round.events[-1]
            if self._event_completes_operation(
                current, event, operation
            ) or self._event_preempts_operation(current, event, operation):
                return current
            screenshot = await self.context.browser.screenshot()
            msg = (
                "Match state changed before the requested operation completed."
            )
            raise ScreenInconsistentMessageError(msg, screenshot)

    @classmethod
    def _matches_seat_indicator(cls, screenshot: object) -> bool:
        return any(
            template.matches(screenshot)
            for template in cls.SEAT_INDICATOR_TEMPLATES
        )

    async def _initialize(self) -> None:
        while self._state_store.state is None:
            message = await self._get_sniffer_message()
            self._apply_match_message(message)

    async def _apply_match_message_with_screen_errors(
        self,
        message: DecodedSnifferMessage,
        *,
        inconsistent_message: str,
    ) -> None:
        try:
            self._apply_match_message(message)
        except MatchMetadataUnsupportedError as error:
            await self._raise_unsupported_match(cause=error)
        except (MatchActionDecodeError, MatchMetadataDecodeError) as error:
            await self._raise_inconsistent_message(
                inconsistent_message,
                cause=error,
            )

    def _apply_match_message(
        self,
        message: DecodedSnifferMessage,
    ) -> None:
        name = message.raw.name
        if name == AUTH_GAME_NAME:
            self._log_sniffer_message(message)
            self._apply_auth_game(message)
            self._try_initialize_state()
            return
        if name != ACTION_PROTOTYPE_NAME:
            self._log_sniffer_message(message)
            return

        if not isinstance(message, DecodedNotice):
            msg = "ActionPrototype must be a Notice."
            raise MatchActionDecodeError(msg)
        event, operation, decoded_message = decode_live_action(message)
        _logger.info(_format_sniffer_message_for_log(decoded_message))
        if self._state_store.state is None:
            self._apply_initialization_event(event, operation)
            self._try_initialize_state()
        else:
            self._apply_active_event(event, operation)
        self._operation_candidates_observed_at = (
            message.raw.observed_at if operation is not None else None
        )

    @staticmethod
    def _log_sniffer_message(
        message: DecodedSnifferMessage,
    ) -> None:
        name = message.raw.name
        formatted_message = _format_sniffer_message_for_log(message)
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

    def _apply_initialization_event(
        self,
        event: MatchEvent,
        operation: _OperationCandidatesSpecification | None,
    ) -> None:
        match event:
            case StartMatchEvent():
                if operation is not None:
                    msg = "ActionMJStart must not contain operations."
                    raise MatchActionDecodeError(msg)
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
                self._new_round_operation_specification = operation
            case (
                ZimoEvent()
                | DapaiEvent()
                | ChiEvent()
                | PengEvent()
                | DaminggangEvent()
                | AngangEvent()
                | JiagangEvent()
                | BabeiEvent()
                | LiujuEvent()
                | HuleEvent()
            ):
                msg = f"{type(event).__name__} must follow ActionNewRound."
                raise MatchActionDecodeError(msg)
            case _ as unreachable:
                assert_never(unreachable)

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
                self._new_round_operation_specification,
            )
        except ValueError as error:
            msg = "Initial match state is inconsistent."
            raise MatchMetadataDecodeError(msg) from error

    def _apply_active_event(
        self,
        event: MatchEvent,
        operation: _OperationCandidatesSpecification | None,
    ) -> None:
        match event:
            case StartMatchEvent() | NewRoundEvent():
                msg = "A match initialization action must not be repeated."
                raise MatchActionDecodeError(msg)
            case _:
                try:
                    self._state_store.apply_event(event, operation)
                except ValueError as error:
                    msg = (
                        f"{type(event).__name__} is inconsistent with "
                        "match state."
                    )
                    raise MatchActionDecodeError(msg) from error

    async def _operate_dapai(
        self,
        state: MatchState,
        operation: DapaiOperation,
    ) -> None:
        round_state = state.round
        is_dealer_first_discard = (
            round_state.ju == state.self_seat
            and round_state.first_draw[state.self_seat]
        )
        if is_dealer_first_discard:
            # Wait for the dealing animation. Moving tiles could turn
            # the intended first discard into a different one.
            await asyncio.sleep(DEALER_FIRST_DISCARD_DELAY_SECONDS)
        else:
            await self._wait_until_dapai_ui_is_ready()

        try:
            region = self._get_dapai_region(
                state,
                operation,
                is_dealer_first_discard=is_dealer_first_discard,
            )
        except ValueError as error:
            await self._raise_inconsistent_message(
                "A discard candidate does not match the hand layout.",
                cause=error,
            )
        await self._click_dapai_until_progress(region)
        await self._move_mouse_away_from_hand()

    async def _wait_until_dapai_ui_is_ready(self) -> None:
        observed_at = self._operation_candidates_observed_at
        if observed_at is None:
            return
        elapsed_seconds = max(0.0, (utc_now() - observed_at).total_seconds())
        remaining_seconds = max(
            0.0,
            DAPAI_UI_READY_DELAY_SECONDS - elapsed_seconds,
        )
        if remaining_seconds > 0.0:
            await asyncio.sleep(remaining_seconds)

    @classmethod
    def _get_dapai_region(
        cls,
        state: MatchState,
        operation: DapaiOperation | LiqiOperation,
        *,
        is_dealer_first_discard: bool,
    ) -> Region:
        round_state = state.round
        use_zimopai_region = operation.moqie or (
            is_dealer_first_discard and round_state.zimopai == operation.tile
        )
        if use_zimopai_region:
            if round_state.zimopai != operation.tile:
                msg = "The discard tile does not match zimopai."
                raise ValueError(msg)
            shoupai_count = len(round_state.shoupai)
            if shoupai_count not in {1, 4, 7, 10, 13}:
                msg = "The hand size has no zimopai display position."
                raise ValueError(msg)
            return cls.ZIMOPAI_REGIONS[(shoupai_count - 1) // 3]

        try:
            index = round_state.shoupai.index(operation.tile)
        except ValueError:
            msg = "The discard tile is not in shoupai."
            raise ValueError(msg) from None
        return Region(
            left=(
                cls.HAND_TILE_REGION.left
                + int(index * cls.HAND_TILE_HORIZONTAL_INTERVAL)
            ),
            top=cls.HAND_TILE_REGION.top,
            width=cls.HAND_TILE_REGION.width,
            height=cls.HAND_TILE_REGION.height,
        )

    async def _click_dapai_until_progress(self, region: Region) -> None:
        loop = asyncio.get_running_loop()
        while True:
            await self.click_region(region)
            retry_at = loop.time() + DAPAI_CLICK_RETRY_INTERVAL_SECONDS
            while True:
                timeout = asyncio.timeout_at(retry_at)
                try:
                    async with timeout:
                        message = await self._get_sniffer_message()
                except TimeoutError:
                    if not timeout.expired():
                        raise
                    break

                if message.raw.name in _DAPAI_CLICK_PROGRESS_MESSAGE_NAMES:
                    self._put_back_sniffer_message(message)
                    return

                await self._apply_match_message_with_screen_errors(
                    message,
                    inconsistent_message=(
                        "Match state update failed while retrying a discard."
                    ),
                )

    async def _operate_chi(
        self,
        state: MatchState,
        operation: ChiOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "ChiOperation requires operation candidates."
            raise RuntimeError(msg)
        chi_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, ChiOperation)
        )
        if not (
            _SINGLE_FULU_CANDIDATE_COUNT
            <= len(chi_operations)
            <= _MAX_CHI_CANDIDATE_COUNT
        ):
            error = ValueError("The number of chi candidates must be 1 to 5.")
            await self._raise_inconsistent_message(
                "Chi candidates do not match the supported UI layout.",
                cause=error,
            )
        await self._operate_chi_peng(
            operation,
            chi_operations,
            self.CHI_BUTTON_TEMPLATE,
        )

    async def _operate_peng(
        self,
        state: MatchState,
        operation: PengOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "PengOperation requires operation candidates."
            raise RuntimeError(msg)
        peng_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, PengOperation)
        )
        if not (
            _SINGLE_FULU_CANDIDATE_COUNT
            <= len(peng_operations)
            <= _MAX_PENG_CANDIDATE_COUNT
        ):
            error = ValueError("The number of peng candidates must be 1 or 2.")
            await self._raise_inconsistent_message(
                "Peng candidates do not match the supported UI layout.",
                cause=error,
            )
        await self._operate_chi_peng(
            operation,
            peng_operations,
            self.PENG_BUTTON_TEMPLATE,
        )

    async def _operate_chi_peng[T: ChiOperation | PengOperation](
        self,
        operation: T,
        operations: tuple[T, ...],
        button_template: TemplateMatcher,
    ) -> None:
        if not await self._click_operation_button_or_detect_progress(
            button_template
        ):
            return

        if len(operations) >= _MIN_MULTIPLE_FULU_CANDIDATE_COUNT:
            index = operations.index(operation)
            selection_region = self._get_chi_peng_combination_region(
                len(operations),
                index,
            )
            await asyncio.sleep(OPERATION_OPTION_DISPLAY_DELAY_SECONDS)
            if await self._put_back_pending_action_while_waiting_for_ui():
                return
            await self.click_region(selection_region)
        await asyncio.sleep(HAND_SLIDE_DELAY_SECONDS)

    @classmethod
    def _get_chi_peng_combination_region(
        cls,
        candidate_count: int,
        index: int,
    ) -> Region:
        if not (
            _MIN_MULTIPLE_FULU_CANDIDATE_COUNT
            <= candidate_count
            <= _MAX_CHI_CANDIDATE_COUNT
        ):
            msg = "Chi/peng combination count must be between 2 and 5."
            raise ValueError(msg)
        if not 0 <= index < candidate_count:
            msg = "Chi/peng combination index is out of range."
            raise ValueError(msg)

        return Region(
            left=(
                cls.CHI_PENG_COMBINATION_REGION.left
                - candidate_count * cls.CHI_PENG_COMBINATION_CENTERING_INTERVAL
                + index * cls.CHI_PENG_COMBINATION_HORIZONTAL_INTERVAL
            ),
            top=cls.CHI_PENG_COMBINATION_REGION.top,
            width=cls.CHI_PENG_COMBINATION_REGION.width,
            height=cls.CHI_PENG_COMBINATION_REGION.height,
        )

    async def _operate_angang(
        self,
        state: MatchState,
        operation: AngangOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "AngangOperation requires operation candidates."
            raise RuntimeError(msg)
        angang_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, AngangOperation)
        )
        if not (
            _SINGLE_FULU_CANDIDATE_COUNT
            <= len(angang_operations)
            <= _MAX_ANGANG_JIAGANG_CANDIDATE_COUNT
        ):
            error = ValueError(
                "The number of angang candidates must be 1 to 3."
            )
            await self._raise_inconsistent_message(
                "Angang candidates do not match the supported UI layout.",
                cause=error,
            )

        await self._operate_angang_jiagang(
            operation,
            angang_operations,
            operation_name="angang",
        )

    async def _operate_daminggang(
        self,
        state: MatchState,
        operation: DaminggangOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "DaminggangOperation requires operation candidates."
            raise RuntimeError(msg)
        daminggang_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, DaminggangOperation)
        )
        if daminggang_operations != (operation,):
            error = ValueError(
                "The number of daminggang candidates must be one."
            )
            await self._raise_inconsistent_message(
                "Daminggang candidates do not match the supported UI layout.",
                cause=error,
            )
        if not await self._click_operation_button_or_detect_progress(
            self.GANG_BUTTON_TEMPLATE
        ):
            return
        await asyncio.sleep(HAND_SLIDE_DELAY_SECONDS)

    async def _operate_jiagang(
        self,
        state: MatchState,
        operation: JiagangOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "JiagangOperation requires operation candidates."
            raise RuntimeError(msg)
        jiagang_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, JiagangOperation)
        )
        if not (
            _SINGLE_FULU_CANDIDATE_COUNT
            <= len(jiagang_operations)
            <= _MAX_ANGANG_JIAGANG_CANDIDATE_COUNT
        ):
            error = ValueError(
                "The number of jiagang candidates must be 1 to 3."
            )
            await self._raise_inconsistent_message(
                "Jiagang candidates do not match the supported UI layout.",
                cause=error,
            )

        await self._operate_angang_jiagang(
            operation,
            jiagang_operations,
            operation_name="jiagang",
        )

    async def _operate_angang_jiagang[T: AngangOperation | JiagangOperation](
        self,
        operation: T,
        operations: tuple[T, ...],
        *,
        operation_name: str,
    ) -> None:
        if not await self._click_operation_button_or_detect_progress(
            self.GANG_BUTTON_TEMPLATE
        ):
            return

        if len(operations) == _SINGLE_FULU_CANDIDATE_COUNT:
            await asyncio.sleep(HAND_SLIDE_DELAY_SECONDS)
            return

        await asyncio.sleep(OPERATION_OPTION_DISPLAY_DELAY_SECONDS)
        if await self._put_back_pending_action_while_waiting_for_ui():
            return

        if len(operations) == _MAX_ANGANG_JIAGANG_CANDIDATE_COUNT:
            screenshot = await self.context.browser.screenshot()
            msg = (
                f"Selecting from three {operation_name} candidates is not "
                "implemented. Please provide the information requested in "
                "the project README."
            )
            raise ScreenNotImplementedOperationError(msg, screenshot)

        index = operations.index(operation)
        await self.click_region(
            self.ANGANG_JIAGANG_TWO_CANDIDATE_REGIONS[index]
        )
        await asyncio.sleep(HAND_SLIDE_DELAY_SECONDS)

    async def _operate_liqi(
        self,
        state: MatchState,
        operation: LiqiOperation,
    ) -> None:
        # The button may not be drawn when its operation message
        # arrives.
        # Wait until it can be clicked or the opportunity disappears.
        while True:
            if await self._put_back_pending_action_while_waiting_for_ui():
                return
            if await self.click_template_if_present(self.LIQI_BUTTON_TEMPLATE):
                break
            await asyncio.sleep(
                OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS
            )

        await asyncio.sleep(OPERATION_OPTION_DISPLAY_DELAY_SECONDS)
        if await self._put_back_pending_action_while_waiting_for_ui():
            return

        round_state = state.round
        is_dealer_first_discard = (
            round_state.ju == state.self_seat
            and round_state.first_draw[state.self_seat]
        )
        try:
            region = self._get_dapai_region(
                state,
                operation,
                is_dealer_first_discard=is_dealer_first_discard,
            )
        except ValueError as error:
            await self._raise_inconsistent_message(
                "A liqi candidate does not match the hand layout.",
                cause=error,
            )
        await self._click_dapai_until_progress(region)
        await self._move_mouse_away_from_hand()

    async def _operate_zimohu(
        self,
        state: MatchState,
        operation: ZimohuOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "ZimohuOperation requires operation candidates."
            raise RuntimeError(msg)
        zimohu_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, ZimohuOperation)
        )
        if zimohu_operations != (operation,):
            error = ValueError("The number of zimohu candidates must be one.")
            await self._raise_inconsistent_message(
                "Zimohu candidates do not match the supported UI layout.",
                cause=error,
            )

        await self._enable_auto_hule(state)

    async def _operate_rong(
        self,
        state: MatchState,
        operation: RongOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "RongOperation requires operation candidates."
            raise RuntimeError(msg)
        rong_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, RongOperation)
        )
        if rong_operations != (operation,):
            error = ValueError("The number of rong candidates must be one.")
            await self._raise_inconsistent_message(
                "Rong candidates do not match the supported UI layout.",
                cause=error,
            )

        await self._enable_auto_hule(state)

    async def _enable_auto_hule(self, state: MatchState) -> None:
        region = (
            self.AUTO_HULE_TOGGLE_SANMA_REGION
            if len(state.players) == 3  # noqa: PLR2004
            else self.AUTO_HULE_TOGGLE_YONMA_REGION
        )
        await self.click_region(region, warp=True)

    async def _operate_liuju(
        self,
        state: MatchState,
        operation: LiujuOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "LiujuOperation requires operation candidates."
            raise RuntimeError(msg)
        liuju_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, LiujuOperation)
        )
        if liuju_operations != (operation,):
            error = ValueError("The number of liuju candidates must be one.")
            await self._raise_inconsistent_message(
                "Liuju candidates do not match the supported UI layout.",
                cause=error,
            )
        if not await self._click_operation_button_or_detect_progress(
            self.LIUJU_BUTTON_TEMPLATE
        ):
            return

    async def _operate_babei(
        self,
        state: MatchState,
        operation: BabeiOperation,
    ) -> None:
        candidates = state.round.operation_candidates
        if candidates is None:
            msg = "BabeiOperation requires operation candidates."
            raise RuntimeError(msg)
        babei_operations = tuple(
            candidate
            for candidate in candidates.operations
            if isinstance(candidate, BabeiOperation)
        )
        if babei_operations != (operation,):
            error = ValueError("The number of babei candidates must be one.")
            await self._raise_inconsistent_message(
                "Babei candidates do not match the supported UI layout.",
                cause=error,
            )
        if not await self._click_operation_button_or_detect_progress(
            self.BABEI_BUTTON_TEMPLATE
        ):
            return
        await asyncio.sleep(HAND_SLIDE_DELAY_SECONDS)

    async def _click_operation_button_or_detect_progress(
        self,
        button_template: TemplateMatcher,
    ) -> bool:
        # Determine whether the operation button can be clicked or the
        # opportunity disappears before the click. The authoritative
        # event is verified later by the normal operation pipeline.
        while True:
            if await self._put_back_pending_action_while_waiting_for_ui():
                return False
            if await self.click_template_if_present(button_template):
                return True
            await asyncio.sleep(
                OPERATION_BUTTON_DETECTION_RETRY_INTERVAL_SECONDS
            )

    async def _put_back_pending_action_while_waiting_for_ui(self) -> bool:
        while (message := self._get_sniffer_message_nowait()) is not None:
            if message.raw.name == ACTION_PROTOTYPE_NAME:
                self._put_back_sniffer_message(message)
                return True
            await self._apply_match_message_with_screen_errors(
                message,
                inconsistent_message=(
                    "Match state update failed while waiting for operation UI."
                ),
            )
        return False

    async def _move_mouse_away_from_hand(self) -> None:
        # Hovering over a tile in the hand can display winning-tile
        # candidates. They may interfere with template matching, so keep
        # the cursor in the empty area immediately above the hand.
        await self.move_region(self.MOUSE_SAFE_REGION)

    @staticmethod
    def _event_completes_operation(
        state: MatchState,
        event: MatchEvent,
        operation: MatchOperation,
    ) -> bool:
        match operation:
            case DapaiOperation():
                return (
                    isinstance(event, DapaiEvent)
                    and event.seat == state.self_seat
                    and event.tile == operation.tile
                    and event.moqie is operation.moqie
                )
            case ChiOperation():
                return (
                    isinstance(event, ChiEvent)
                    and event.seat == state.self_seat
                    and event.from_seat == operation.from_seat
                    and event.tile == operation.tile
                    and event.consumed == operation.consumed
                )
            case PengOperation():
                return (
                    isinstance(event, PengEvent)
                    and event.seat == state.self_seat
                    and event.from_seat == operation.from_seat
                    and event.tile == operation.tile
                    and event.consumed == operation.consumed
                )
            case AngangOperation():
                return (
                    isinstance(event, AngangEvent)
                    and event.seat == state.self_seat
                    and normalize_tile_kind(event.consumed[0])
                    == normalize_tile_kind(operation.consumed[0])
                )
            case DaminggangOperation():
                return (
                    isinstance(event, DaminggangEvent)
                    and event.seat == state.self_seat
                    and event.from_seat == operation.from_seat
                    and event.tile == operation.tile
                    and event.consumed == operation.consumed
                )
            case JiagangOperation():
                return (
                    isinstance(event, JiagangEvent)
                    and event.seat == state.self_seat
                    and event.added == operation.added
                )
            case LiqiOperation():
                return (
                    isinstance(event, DapaiEvent)
                    and event.seat == state.self_seat
                    and event.tile == operation.tile
                    and event.moqie is operation.moqie
                    and (event.liqi or event.wliqi)
                )
            case ZimohuOperation():
                return (
                    isinstance(event, HuleEvent)
                    and len(event.hules) == 1
                    and event.hules[0].seat == state.self_seat
                    and event.hules[0].zimo
                    and event.hules[0].hu_tile == operation.tile
                )
            case RongOperation():
                return isinstance(event, HuleEvent) and any(
                    hule.seat == state.self_seat
                    and not hule.zimo
                    and hule.hu_tile == operation.tile
                    for hule in event.hules
                )
            case LiujuOperation():
                return (
                    isinstance(event, LiujuEvent)
                    and event.type is LiujuType.JIUZHONGJIUPAI
                    and event.seat == state.self_seat
                )
            case BabeiOperation():
                return (
                    isinstance(event, BabeiEvent)
                    and event.seat == state.self_seat
                )
        assert_never(operation)

    @staticmethod
    def _event_preempts_operation(
        state: MatchState,
        event: MatchEvent,
        operation: MatchOperation,
    ) -> bool:
        is_opponents_hule = isinstance(event, HuleEvent) and all(
            hule.seat != state.self_seat for hule in event.hules
        )
        match operation:
            case ChiOperation():
                return (
                    isinstance(event, PengEvent | DaminggangEvent)
                    and event.seat != state.self_seat
                ) or is_opponents_hule
            case PengOperation() | DaminggangOperation():
                return is_opponents_hule
            case (
                DapaiOperation()
                | AngangOperation()
                | JiagangOperation()
                | LiqiOperation()
                | ZimohuOperation()
                | RongOperation()
                | LiujuOperation()
                | BabeiOperation()
            ):
                return False
        assert_never(operation)

    async def _raise_inconsistent_message(
        self,
        message: str,
        *,
        cause: BaseException,
    ) -> NoReturn:
        screenshot = await self.context.browser.screenshot()
        raise ScreenInconsistentMessageError(message, screenshot) from cause

    async def _raise_unsupported_match(
        self,
        *,
        cause: BaseException,
    ) -> NoReturn:
        screenshot = await self.context.browser.screenshot()
        msg = "The detected match type is not supported."
        raise ScreenUnexpectedStateError(msg, screenshot) from cause
