# ruff: noqa: C901, PLR2004, S101
import datetime
import time
from logging import getLogger
from typing import Any, TypeGuard

from majsoulrpa._impl import id
from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import (
    Message,
    MessageQueueClientBase,
)
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline, to_timedelta
from majsoulrpa.presentation.exceptions import (
    BrowserRefreshRequest,
    InconsistentMessageError,
    InvalidOperationError,
    NotImplementedOperationError,
    PresentationNotDetectedError,
    PresentationTimeoutError,
    UnexpectedStateError,
)
from majsoulrpa.presentation.match.event import (
    AngangJiagangEvent,
    BabeiEvent,
    ChiPengGangEvent,
    DapaiEvent,
    HuleEvent,
    LiujuEvent,
    NewRoundEvent,
    NoTileEvent,
    ZimoEvent,
)
from majsoulrpa.presentation.match.event._base import EventBase
from majsoulrpa.presentation.match.operation import (
    AngangOperation,
    BabeiOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    JiagangOperation,
    JiuzhongjiupaiOperation,
    LiqiOperation,
    OperationBase,
    OperationList,
    PengOperation,
    RongOperation,
    ZimohuOperation,
)
from majsoulrpa.presentation.match.state import (
    MatchPlayer,
    MatchState,
    RoundState,
)
from majsoulrpa.presentation.presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)

from . import _common

logger = getLogger(__name__)


class MatchPresentation(PresentationBase):
    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 60.0) -> None:
        deadline = timeout_to_deadline(timeout)
        paths = [f"template/match/marker{i}" for i in range(4)]
        templates = [Template.open_file(p, browser.zoom_ratio) for p in paths]
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise PresentationTimeoutError(msg, browser.get_screenshot())
            if (
                Template.match_one_of(browser.get_screenshot(), templates)
                != -1
            ):
                break

    _COMMON_MESSAGE_NAMES = (
        ".lq.Lobby.heatbeat",
        ".lq.Lobby.loginBeat",
        ".lq.Lobby.fetchServerTime",
        ".lq.NotifyReviveCoinUpdate",
        ".lq.NotifyGiftSendRefresh",
        ".lq.NotifyDailyTaskUpdate",
        ".lq.NotifyShopUpdate",
        ".lq.NotifyAccountChallengeTaskUpdate",
        ".lq.NotifyAccountUpdate",
        ".lq.Lobby.fetchShopInterval",
        ".lq.Lobby.fetchActivityInterval",
        ".lq.NotifyActivityChange",
        ".lq.NotifyActivityTaskUpdate",
        ".lq.NotifyAnnouncementUpdate",
        ".lq.FastTest.authGame",
        ".lq.Lobby.oauth2Login",
        ".lq.FastTest.checkNetworkDelay",
        ".lq.FastTest.fetchGamePlayerState",
        ".lq.NotifyPlayerConnectionState",
        ".lq.NotifyGameBroadcast",
        ".lq.PlayerLeaving",
    )

    def _on_common_message(self, message: Message) -> None:
        _, name, request, _, _ = message

        match name:
            case ".lq.Lobby.heatbeat":
                # frequently exchanged
                logger.debug(message)
                return
            case ".lq.Lobby.loginBeat":
                # rarely exchanged
                logger.warning(message)
                return
            case ".lq.Lobby.fetchServerTime":
                # occasionally exchanged
                logger.info(message)
                return
            case (
                ".lq.NotifyReviveCoinUpdate"
                | ".lq.NotifyGiftSendRefresh"
                | ".lq.NotifyDailyTaskUpdate"
                | ".lq.NotifyShopUpdate"
                | ".lq.NotifyAccountChallengeTaskUpdate"
                | ".lq.NotifyAccountUpdate"
                | ".lq.Lobby.fetchShopInterval"
                | ".lq.Lobby.fetchActivityInterval"
                | ".lq.NotifyActivityChange"  # only during events?
                | ".lq.NotifyActivityTaskUpdate"  # only during events?
            ):
                # Exchanged if the date (06:00:00 (UTC+0900)) is crossed
                logger.info(message)
                return
            case ".lq.NotifyAnnouncementUpdate":
                # Will be exchanged if there is an update to the notice
                logger.info(message)
                return
            case ".lq.FastTest.authGame":
                # Rarely exchanged during the game
                logger.info(message)
                return
            case ".lq.Lobby.oauth2Login":
                logger.warning(message)
                if request["reconnect"]:
                    # When reconnecting after
                    # communication is disconnected
                    return
                raise InconsistentMessageError(str(message))
            case ".lq.FastTest.checkNetworkDelay":
                # frequently exchanged
                logger.debug(message)
                return
            case (
                ".lq.FastTest.fetchGamePlayerState"
                | ".lq.NotifyPlayerConnectionState"
            ):
                logger.info(message)
                # TODO: Checking the connection status of each player
                return
            case ".lq.NotifyGameBroadcast":
                # TODO: Stamp and other processing
                logger.info(message)
                return
            case ".lq.PlayerLeaving":
                # TODO: What to do when judged to be out of seat
                logger.info(message)
                return

        raise AssertionError(message)

    def _on_auth_game(self, message: Message) -> None:
        _, _, request, response, _ = message

        uuid = request["game_uuid"]
        self._match_state._set_uuid(uuid)  # noqa: SLF001

        # TODO: Check game settings

        if response is None:
            msg = "`.lq.FastTest.authGame` has no response message."
            raise InconsistentMessageError(msg, self._browser.get_screenshot())

        player_map = {}
        for p in response["players"]:
            account_id = p["account_id"]
            nickname = p["nickname"]
            level4 = id.id_to_level(p["level"]["id"])
            level3 = id.id_to_level(p["level3"]["id"])
            charid = p["character"]["charid"]

            try:
                character = id.id_to_character(charid)
            except KeyError:
                # When encountering a character whose
                # character ID is unknown
                logger.warning("%s: %s: charid = %s", uuid, nickname, charid)
                character = "UNKNOWN"

            player_map[account_id] = MatchPlayer(
                account_id,
                nickname,
                level4,
                level3,
                character,
            )

        players = []
        for i in range(len(response["seat_list"])):
            account_id = response["seat_list"][i]
            if account_id == self._message_queue_client.account_id:
                self._match_state._set_seat(i)  # noqa: SLF001
            if account_id == 0:
                player = MatchPlayer(0, "CPU", "初心1", "初心1", "一姫")
                players.append(player)
            else:
                players.append(player_map[account_id])
        self._match_state._set_players(players)  # noqa: SLF001

    def _on_sync_game(self, message: Message, *, restore: bool) -> None:
        direction, name, request, response, timestamp = message
        if direction != "outbound":
            raise ValueError(message)
        if name != ".lq.FastTest.syncGame":
            raise ValueError(message)

        if restore:
            if request["round_id"] != "-1":
                raise InconsistentMessageError(str(message))
            if request["step"] != 1000000:
                raise InconsistentMessageError(str(message))
        else:
            if request["round_id"] != f"{self.chang}-{self.ju}-{self.ben}":
                raise InconsistentMessageError(str(message))
            if request["step"] != 4294967295:
                raise InconsistentMessageError(str(message))

        if response is None:
            raise InconsistentMessageError(str(message))

        game_restore = response["game_restore"]

        if game_restore["game_state"] != 1:
            raise NotImplementedError(message)

        actions: list[Any] = game_restore["actions"]
        if len(actions) == 0:
            raise InconsistentMessageError(str(message))
        if len(actions) != response["step"]:
            raise InconsistentMessageError(str(message))

        action = actions.pop(0)
        step, name, data = _common.parse_action(action, restore=True)
        self._step = 0

        if step != 0:
            raise InconsistentMessageError(str(action))

        if name == "ActionMJStart":
            if len(actions) == 0:
                raise InconsistentMessageError(str(message))

            action = actions.pop(0)
            step, name, data = _common.parse_action(action, restore=True)
            if step != 1:
                raise InconsistentMessageError(str(action))
            self._step += 1

        if name != "ActionNewRound":
            raise InconsistentMessageError(str(action))

        self._events.clear()
        self._events.append(NewRoundEvent(data, timestamp))
        self._round_state = RoundState(self._match_state, data)
        self._operation_list = None
        if ("operation" in data) and len(
            data["operation"]["operation_list"],
        ) > 0:
            self._operation_list = OperationList(data["operation"])
        else:
            self._operation_list = None
        self._step += 1

        for action in actions:
            step, name, data = _common.parse_action(action, restore=True)
            if step != self._step:
                raise InconsistentMessageError(str(action))

            match name:
                case "ActionDealTile":
                    self._events.append(ZimoEvent(data, timestamp))
                    self._round_state._on_zimo(data)  # noqa: SLF001
                    if ("operation" in data) and len(
                        data["operation"]["operation_list"],
                    ) > 0:
                        self._operation_list = OperationList(data["operation"])
                    else:
                        self._operation_list = None
                    self._step += 1
                case "ActionDiscardTile":
                    self._events.append(DapaiEvent(data, timestamp))
                    self._round_state._on_dapai(data)  # noqa: SLF001
                    if ("operation" in data) and len(
                        data["operation"]["operation_list"],
                    ) > 0:
                        self._operation_list = OperationList(data["operation"])
                    else:
                        self._operation_list = None
                    self._step += 1
                case "ActionChiPengGang":
                    self._events.append(ChiPengGangEvent(data, timestamp))
                    self._round_state._on_chipenggang(data)  # noqa: SLF001
                    if ("operation" in data) and len(
                        data["operation"]["operation_list"],
                    ) > 0:
                        self._operation_list = OperationList(data["operation"])
                    else:
                        self._operation_list = None
                    self._step += 1
                case "ActionAnGangAddGang":
                    self._events.append(AngangJiagangEvent(data, timestamp))
                    self._round_state._on_angang_jiagang(data)  # noqa: SLF001
                    if ("operation" in data) and len(
                        data["operation"]["operation_list"],
                    ) > 0:
                        self._operation_list = OperationList(data["operation"])
                    else:
                        self._operation_list = None
                    self._step += 1
                case "ActionBaBei":
                    self._events.append(BabeiEvent(data, timestamp))
                    self._round_state._on_babei(data)  # noqa: SLF001
                    if ("operation" in data) and len(
                        data["operation"]["operation_list"],
                    ) > 0:
                        self._operation_list = OperationList(data["operation"])
                    else:
                        self._operation_list = None
                    self._step += 1
                case "ActionHule":
                    raise InconsistentMessageError(str(action))
                case "ActionNoTile":
                    raise InconsistentMessageError(str(action))
                case "ActionLiuJu":
                    raise InconsistentMessageError(str(action))
                case _:
                    raise InconsistentMessageError(str(action))

    def _restore(self, screenshot: bytes, deadline: datetime.datetime) -> None:
        is_received_auth_game = False
        is_received_sync_game = False

        while True:
            message = self._message_queue_client.dequeue_message(
                deadline - datetime.datetime.now(datetime.UTC),
            )
            if message is None:
                msg = "Timeout"
                raise PresentationTimeoutError(msg, screenshot)
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.Lobby.heatbeat"
                    | ".lq.Lobby.oauth2Auth"
                    | ".lq.Lobby.oauth2Check"
                    | ".lq.Lobby.oauth2Login"
                    | ".lq.Lobby.fetchLastPrivacy"
                    | ".lq.Lobby.fetchServerTime"
                    | ".lq.Lobby.fetchServerSettings"
                    | ".lq.Lobby.fetchConnectionInfo"
                    | ".lq.Lobby.fetchClientValue"
                    | ".lq.Lobby.fetchFriendList"
                    | ".lq.Lobby.fetchFriendApplyList"
                    | ".lq.Lobby.fetchRecentFriend"
                    | ".lq.Lobby.fetchMailInfo"
                    | ".lq.Lobby.fetchDailyTask"
                    | ".lq.Lobby.fetchReviveCoinInfo"
                    | ".lq.Lobby.fetchTitleList"
                    | ".lq.Lobby.fetchBagInfo"
                    | ".lq.Lobby.fetchShopInfo"
                    | ".lq.Lobby.fetchShopInterval"
                    | ".lq.Lobby.fetchActivityList"
                    | ".lq.Lobby.fetchActivityInterval"
                    | ".lq.Lobby.fetchAccountActivityData"
                    | ".lq.Lobby.fetchActivityBuff"
                    | ".lq.Lobby.fetchVipReward"
                    | ".lq.Lobby.fetchMonthTicketInfo"
                    | ".lq.Lobby.fetchAchievement"
                    | ".lq.Lobby.fetchCommentSetting"
                    | ".lq.Lobby.fetchAccountSettings"
                    | ".lq.Lobby.fetchModNicknameTime"
                    | ".lq.Lobby.fetchMisc"
                    | ".lq.Lobby.fetchAnnouncement"
                    | ".lq.Lobby.fetchRollingNotice"
                    | ".lq.NotifyAccountUpdate"
                    | ".lq.Lobby.loginSuccess"
                    | ".lq.Lobby.fetchCharacterInfo"
                    | ".lq.Lobby.fetchAllCommonViews"
                    | ".lq.Lobby.fetchInfo"
                    | ".lq.FastTest.checkNetworkDelay"
                    | ".lq.FastTest.fetchGamePlayerState"
                    | ".lq.FastTest.finishSyncGame"
                ):
                    logger.info(message)
                case ".lq.FastTest.authGame":
                    logger.info(message)
                    self._on_auth_game(message)
                    is_received_auth_game = True
                case ".lq.FastTest.syncGame":
                    logger.info(message)
                    self._on_sync_game(message, restore=True)
                    is_received_sync_game = True
                case (
                    ".lq.ActionPrototype"
                    | ".lq.FastTest.inputOperation"
                    | ".lq.FastTest.inputChiPengGang"
                ):
                    self._message_queue_client.put_back(message)
                    break
                case _:
                    raise InconsistentMessageError(str(message), screenshot)

            if is_received_sync_game and is_received_auth_game:
                next_message = self._message_queue_client.dequeue_message(1)
                if next_message is None:
                    # If there are no more messages, it is waiting for
                    # an operation on own turn.
                    break
                self._message_queue_client.put_back(next_message)

    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        prev_presentation: Presentation | None,
        timeout: TimeoutType = 60.0,
        *,
        match_state: MatchState | None = None,
    ) -> None:
        super().__init__(browser, message_queue_client, creator)

        self._prev_presentation = prev_presentation
        self._step = 0
        self._events: list[EventBase] = []
        if match_state is None:
            match_state = MatchState()
        self._match_state = match_state
        self._operation_list = None

        # If the mouse cursor is placed over the tiles in the hand,
        # winning tile candidates may be displayed and interfere with
        # template matching. Therefore, move the mouse cursor to an
        # appropriate position where there are no tiles in the hand.
        self._browser.move_to_region(
            int(986 * self._browser.zoom_ratio),
            int(806 * self._browser.zoom_ratio),
            int(134 * self._browser.zoom_ratio),
            int(57 * self._browser.zoom_ratio),
            edge_sigma=1.0,
        )

        paths = [f"template/match/marker{i}" for i in range(4)]
        templates = [Template.open_file(p, browser.zoom_ratio) for p in paths]
        ss = browser.get_screenshot()
        if Template.match_one_of(ss, templates) == -1:
            msg = "Could not detect `match_main`."
            raise PresentationNotDetectedError(msg, ss)

        deadline = timeout_to_deadline(timeout)

        if self._prev_presentation is None:
            self._restore(ss, deadline)
            # As a temporary workaround,
            # set _prev_presentation to ROOM_GUEST
            # TODO: Refactor for a proper solution later
            self._prev_presentation = Presentation.ROOM_GUEST
            return

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout."
                raise PresentationTimeoutError(msg, ss)
            _, name, request, _, timestamp = message

            match name:
                case ".lq.Lobby.fetchCustomizedContestOnlineInfo":
                    # exchanged regularly in the tournament room
                    logger.info(message)
                    continue
                case ".lq.Lobby.startCustomizedContest":
                    # exchanged when clicking on "Prepare for match"
                    logger.info(message)
                    continue
                case ".lq.Lobby.stopCustomizedContest":
                    # exchanged when clicking on "Waiting to start..."
                    logger.info(message)
                    continue
                case (
                    ".lq.NotifyCustomContestSystemMsg"
                    | ".lq.Lobby.leaveCustomizedContestChatRoom"
                ):
                    # Tournament match starts.
                    logger.info(message)
                    continue
                case ".lq.Lobby.modifyRoom":
                    # If an API response message regarding changing
                    # the friendly match waiting room is returned
                    # after the friendly match has started.
                    logger.info(message)
                    continue
                case (
                    ".lq.NotifyRoomPlayerUpdate"
                    | ".lq.NotifyRoomPlayerReady"
                ):
                    # If change notification for
                    # the friendly match waiting room was sent
                    # after the friendly match has started.
                    logger.info(message)
                    continue
                case ".lq.NotifyRoomGameStart":
                    # Tournament match or friendly match starts.
                    logger.info(message)
                    uuid = request["game_uuid"]
                    self._match_state._set_uuid(uuid)  # noqa: SLF001
                    continue
                case ".lq.Lobby.startRoom":
                    logger.info(message)
                    continue
                case ".lq.FastTest.authGame":
                    logger.info(message)
                    self._on_auth_game(message)
                    continue
                case ".lq.FastTest.enterGame":
                    # TODO: Resume process for interrupted matches?
                    logger.debug(message)
                    continue
                case ".lq.NotifyPlayerLoadGameReady":
                    logger.info(message)
                    continue
                case ".lq.ActionPrototype":
                    step, action_name, data = _common.parse_action(request)
                    action_info = {
                        "step": step,
                        "action_name": action_name,
                        "data": data,
                    }
                    if step != self._step:
                        raise InconsistentMessageError(str(action_info), ss)
                    self._step += 1

                    if action_name == "ActionMJStart":
                        logger.info(action_info)
                        continue

                    if action_name == "ActionNewRound":
                        logger.info(action_info)
                        self._events.append(NewRoundEvent(data, timestamp))
                        self._round_state = RoundState(self._match_state, data)
                        if "operation" in data:
                            if len(data["operation"]["operation_list"]) == 0:
                                return
                            self._operation_list = OperationList(
                                data["operation"],
                            )
                        return

                    raise InconsistentMessageError(str(action_info), ss)

            # The conditional statement regarding
            # `.lq.FastTest.authGame` must come before this conditional
            # statement.
            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            raise InconsistentMessageError(str(message), ss)

    @property
    def uuid(self) -> str:
        return self._match_state.uuid

    @property
    def seat(self) -> int:
        return self._match_state.seat

    @property
    def players(self) -> list[MatchPlayer]:
        return self._match_state.players

    @property
    def chang(self) -> int:
        return self._round_state.chang

    @property
    def ju(self) -> int:
        return self._round_state.ju

    @property
    def ben(self) -> int:
        return self._round_state.ben

    @property
    def liqibang(self) -> int:
        return self._round_state.liqibang

    @property
    def dora_indicators(self) -> list[str]:
        return self._round_state.dora_indicators

    @property
    def left_tile_count(self) -> int:
        return self._round_state.left_tile_count

    @property
    def scores(self) -> list[int]:
        return self._round_state.scores

    @property
    def shoupai(self) -> list[str]:
        return self._round_state.shoupai

    @property
    def zimopai(self) -> str | None:
        return self._round_state.zimopai

    @property
    def he(self) -> list[list[tuple[str, bool]]]:
        return self._round_state.he

    @property
    def fulu(
        self,
    ) -> list[list[tuple[str, int | None, int | None, list[str]]]]:
        return self._round_state.fulu

    @property
    def num_babei(self) -> list[int]:
        return self._round_state.num_babei

    @property
    def liqi(self) -> list[bool]:
        return self._round_state.liqi

    @property
    def wliqi(self) -> list[bool]:
        return self._round_state.wliqi

    @property
    def first_draw(self) -> bool:
        return self._round_state.first_draw[self.seat]

    @property
    def yifa(self) -> list[bool]:
        return self._round_state.yifa

    @property
    def lingshang_zimo(self) -> bool:
        return self._round_state.lingshang_zimo[self.seat]

    @property
    def prev_dapai_seat(self) -> int | None:
        return self._round_state.prev_dapai_seat

    @property
    def prev_dapai(self) -> str | None:
        return self._round_state.prev_dapai

    @property
    def operation_list(self) -> OperationList | None:
        return self._operation_list

    @property
    def events(self) -> list[EventBase]:
        return self._events

    def _robust_click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        interval: TimeoutType,
        timeout: TimeoutType,
        edge_sigma: float = 2.0,
    ) -> None:
        interval = to_timedelta(interval)

        deadline = timeout_to_deadline(timeout)
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )

            self._browser.click_region(left, top, width, height, edge_sigma)
            message = self._message_queue_client.dequeue_message(interval)
            if message is None:
                continue
            _, name, _, _, _ = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            match name:
                case (
                    ".lq.FastTest.inputOperation"
                    | ".lq.FastTest.inputChiPengGang"
                    | ".lq.ActionPrototype"
                ):
                    break

            raise InconsistentMessageError(
                str(message),
                self._browser.get_screenshot(),
            )

        # Backfill the prefetched message.
        self._message_queue_client.put_back(message)

    def _reset_to_prev_presentation(self, deadline: datetime.datetime) -> None:
        # If there is an additional "confirm" button
        # such as when receiving rewards, click it.
        template = Template.open_file(
            "template/match/match_result_confirm",
            self._browser.zoom_ratio,
        )
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout"
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
            try:
                template.wait_for_then_click(self._browser, 5.0)
            except PresentationTimeoutError:
                break

        if self._prev_presentation == Presentation.TOURNAMENT:
            now = datetime.datetime.now(datetime.UTC)
            self._creator.wait(
                self._browser,
                deadline - now,
                self._prev_presentation,
            )
            now = datetime.datetime.now(datetime.UTC)
            new_presentation = self._creator.create_new_presentation(
                Presentation.MATCH,
                self._prev_presentation,
                self._browser,
                self._message_queue_client,
            )
            self._set_new_presentation(new_presentation)
            return

        if self._prev_presentation in (
            Presentation.ROOM_HOST,
            Presentation.ROOM_GUEST,
        ):
            now = datetime.datetime.now(datetime.UTC)
            self._creator.wait(
                self._browser,
                deadline - now,
                self._prev_presentation,
            )
            now = datetime.datetime.now(datetime.UTC)
            new_presentation = self._creator.create_new_presentation(
                Presentation.MATCH,
                self._prev_presentation,
                self._browser,
                self._message_queue_client,
                timeout=(deadline - now),
            )
            self._set_new_presentation(new_presentation)
            return

        # TODO: What to do when restarting a suspended match.
        # In this case, `self._prev_presentation` is `None`.
        if self._prev_presentation is None:
            raise NotImplementedError(self._prev_presentation)
        raise NotImplementedError(self._prev_presentation.name)

    def _obtain_event_reward(self, deadline: datetime.datetime) -> None:
        # Clicks on the screen until the "Confirm" button
        # is displayed when obtaining the event reward.
        template = Template.open_file(
            "template/match/match_result_confirm",
            self._browser.zoom_ratio,
        )
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout"
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
            if template.match(self._browser.get_screenshot()):
                break
            # Avoid clicking the "Confirm" button by accident.
            self._browser.click_region(
                0,
                0,
                int(1625 * self._browser.zoom_ratio),
                int(952 * self._browser.zoom_ratio),
            )

    def _on_end_of_match(self, deadline: datetime.datetime) -> None:
        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout"
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
            _, name, _, _, _ = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            match name:
                case ".lq.FastTest.inputChiPengGang":
                    # The response message of
                    # `.lq.FastTest.inputChiPengGang`
                    # may be returned late,
                    # so there is a workaround for this.
                    logger.info(message)
                    continue
                case ".lq.Lobby.fetchAccountInfo":
                    logger.info(message)
                    # TODO: Processing message content
                    # Apparently only during an event.
                    # If there are no more messages,
                    # return to the home screen
                    message = self._message_queue_client.dequeue_message(5)
                    if message is None:
                        self._reset_to_prev_presentation(deadline)
                        return

                    # Backfill the prefetched message and
                    # proceed to the next.
                    self._message_queue_client.put_back(message)
                    continue
                case (
                    ".lq.NotifyAccountUpdate"
                    | ".lq.NotifyGameFinishReward"
                    | ".lq.NotifyActivityReward"
                    | ".lq.NotifyActivityPoint"
                    | ".lq.NotifyLeaderboardPoint"
                ):
                    logger.info(message)
                    # TODO: Processing message content
                    continue
                case ".lq.NotifyActivityRewardV2":
                    logger.info(message)
                    self._obtain_event_reward(deadline)
                    continue
                case ".lq.NotifyActivityPointV2":
                    logger.info(message)
                    # TODO: Processing message content

                    # If there are no more messages,
                    # return to the home screen
                    message = self._message_queue_client.dequeue_message(5)
                    if message is None:
                        self._reset_to_prev_presentation(deadline)
                        return

                    # Backfill the prefetched message and
                    # proceed to the next.
                    self._message_queue_client.put_back(message)
                    continue
                case (
                    ".lq.Lobby.enterCustomizedContest"
                    | ".lq.Lobby.joinCustomizedContestChatRoom"
                    | ".lq.Lobby.fetchCustomizedContestOnlineInfo"
                ):
                    # Return to tournament match room.
                    # Backfill the prefetched message.
                    self._message_queue_client.put_back(message)
                    self._reset_to_prev_presentation(deadline)
                    return
                case ".lq.Lobby.fetchRoom":
                    # Return to friendly match room.
                    # Backfill the prefetched message.
                    self._message_queue_client.put_back(message)
                    self._reset_to_prev_presentation(deadline)
                    return
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    )

    def _workaround_for_reordered_actions(
        self,
        message: Message | None,
        expected_step: int,
        timeout: TimeoutType,
    ) -> Message:
        # Since `.lq.ActionPrototype` may not come in
        # the `step` order, read ahead the messages and
        # sort them in the `step` order.
        if message is None:
            msg = "`message` is `None`."
            raise ValueError(msg)
        if message[1] != ".lq.ActionPrototype":
            raise ValueError(message)

        if expected_step < 0:
            raise ValueError(expected_step)

        deadline = timeout_to_deadline(timeout)

        messages: list[Message | None] = []

        def is_no_none_in_messages(
            messages: list[Message | None],
        ) -> TypeGuard[list[Message]]:
            return None not in messages

        while True:
            assert message is not None
            _, name, request, _, _ = message

            flag = False

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                flag = True

            if name == ".lq.ActionPrototype":
                step, action_name, data = _common.parse_action(request)
                action_info: dict[str, int | str | dict] | None = {
                    "step": step,
                    "action_name": action_name,
                    "data": data,
                }
                if step < expected_step:
                    raise InconsistentMessageError(
                        str(action_info),
                        self._browser.get_screenshot(),
                    )
                while len(messages) <= step - expected_step:
                    messages.append(None)
                messages[step - expected_step] = message

                if is_no_none_in_messages(messages):
                    result = messages.pop(0)
                    while len(messages) > 0:
                        message = messages.pop(-1)
                        self._message_queue_client.put_back(message)
                    return result
                flag = True

            if not flag:
                action_infos: list[object] = []
                for m in messages:
                    if m is None:
                        action_info = None
                    else:
                        _, name, request, _, _ = m
                        assert name == ".lq.ActionPrototype"
                        step, action_name, data = _common.parse_action(request)
                        action_info = {
                            "step": step,
                            "action_name": action_name,
                            "data": data,
                        }
                    action_infos.append(action_info)
                error_message = {
                    "expected_step": expected_step,
                    "actions": action_infos,
                    "message": message,
                }
                raise InconsistentMessageError(
                    str(error_message),
                    self._browser.get_screenshot(),
                )

            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout."
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )

    def _workaround_for_skipped_confirm_new_round(
        self,
        message: Message,
        deadline: datetime.datetime,
    ) -> None:
        # Workaround if the `.lq.FastTest.confirmNewRound`
        # interaction is skipped.
        # In this case, the next station's `.lq.ActionPrototype`
        # messages may not arrive in `step` order,
        # so we also do a workaround to sort them in `step` order.
        if message is None:
            msg = "`message` is `None`."
            raise ValueError(msg)
        _, name, request, _, _ = message
        if name != ".lq.ActionPrototype":
            raise InconsistentMessageError(
                str(message),
                self._browser.get_screenshot(),
            )

        step, action_name, _ = _common.parse_action(request)
        if step != 0:
            now = datetime.datetime.now(datetime.UTC)
            message = self._workaround_for_reordered_actions(
                message,
                0,
                deadline - now,
            )

        assert message is not None
        _, name, request, _, _ = message
        assert name == ".lq.ActionPrototype"
        step, action_name, _ = _common.parse_action(request)
        assert step == 0
        assert action_name == "ActionNewRound"
        self._message_queue_client.put_back(message)

        now = datetime.datetime.now(datetime.UTC)
        MatchPresentation._wait(self._browser, deadline - now)
        now = datetime.datetime.now(datetime.UTC)
        new_presentation = MatchPresentation(
            self._browser,
            self._message_queue_client,
            self._creator,
            self._prev_presentation,
            deadline - now,
            match_state=self._match_state,
        )
        self._set_new_presentation(new_presentation)

    def _on_end_of_round(self, deadline: datetime.datetime) -> None:
        template = Template.open_file(
            "template/match/round_result_confirm",
            self._browser.zoom_ratio,
        )
        round_result_confirmed = False
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )

            if not round_result_confirmed:  # noqa: SIM102
                if template.click_if_match(self._browser):
                    round_result_confirmed = True

            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                continue
            _, name, request, _, _ = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            match name:
                case ".lq.FastTest.inputOperation":
                    # The response message of
                    # `.lq.FastTest.inputOperation` may be
                    # returned late, so there is a workaround for this.
                    logger.info(message)
                    continue
                case ".lq.FastTest.inputChiPengGang":
                    # The response message of
                    # `.lq.FastTest.inputChiPengGang` may be
                    # returned late, so there is a workaround for this.
                    logger.info(message)
                    continue
                case ".lq.NotifyActivityChange":
                    logger.info(message)
                    # TODO: Parsing message content
                    continue

            if name == ".lq.FastTest.confirmNewRound":
                # At the end of the round (if there is a next round)
                logger.info(message)
                while True:
                    # Wait for `ActionNewRound` message.
                    now = datetime.datetime.now(datetime.UTC)
                    message = self._message_queue_client.dequeue_message(
                        deadline - now,
                    )
                    if message is None:
                        msg = "Timeout"
                        raise PresentationTimeoutError(
                            msg,
                            self._browser.get_screenshot(),
                        )
                    _, name, request, _, _ = message
                    if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                        self._on_common_message(message)
                        continue
                    if name == ".lq.ActionPrototype":
                        step, action_name, data = _common.parse_action(request)
                        action_info = {
                            "step": step,
                            "action_name": action_name,
                            "data": data,
                        }
                        if action_name == "ActionNewRound":
                            # Backfill the prefetched message.
                            self._message_queue_client.put_back(message)
                            break
                        raise InconsistentMessageError(
                            str(action_info),
                            self._browser.get_screenshot(),
                        )
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    )

                now = datetime.datetime.now(datetime.UTC)
                MatchPresentation._wait(self._browser, deadline - now)
                now = datetime.datetime.now(datetime.UTC)
                new_presentation = MatchPresentation(
                    self._browser,
                    self._message_queue_client,
                    self._creator,
                    self._prev_presentation,
                    deadline - now,
                    match_state=self._match_state,
                )
                self._set_new_presentation(new_presentation)
                return

            if name == ".lq.ActionPrototype":
                # The order of the `.lq.FastTest.confirmNewRound`
                # response message and the `ActionNewRound`
                # message may be reversed,
                # so here is a workaround for that case.
                step, action_name, data = _common.parse_action(request)
                if action_name != "ActionNewRound":
                    raise InconsistentMessageError(
                        str(
                            {
                                "step": step,
                                "action_name": action_name,
                                "data": data,
                            },
                        ),
                        self._browser.get_screenshot(),
                    )
                while True:
                    # Wait for response message of
                    # `.lq.FastTest.confirmNewRound`
                    now = datetime.datetime.now(datetime.UTC)
                    next_message = self._message_queue_client.dequeue_message(
                        deadline - now,
                    )
                    if next_message is None:
                        msg = "Timeout"
                        raise PresentationTimeoutError(
                            msg,
                            self._browser.get_screenshot(),
                        )
                    _, next_name, _, _, _ = next_message
                    if next_name in MatchPresentation._COMMON_MESSAGE_NAMES:
                        self._on_common_message(next_message)
                        continue
                    if next_name == ".lq.ActionPrototype":
                        # The exchange between
                        # `.lq.FastTest.confirmNewRound` and
                        # `ActionNewRound` may be skipped and
                        # `.lq.ActionPrototype` of the next game's
                        # `step = 1` is sent, so here is a workaround
                        # for this phenomenon.
                        # Backfill the prefetched message.
                        self._message_queue_client.put_back(next_message)
                        self._workaround_for_skipped_confirm_new_round(
                            message,
                            deadline,
                        )
                        return
                    if next_name == ".lq.FastTest.confirmNewRound":
                        logger.info(next_name)
                        break
                    if data["ju"] == self.seat:
                        # If you are the parent of the next game.
                        # In extremely rare circumstances,
                        # is there a case where
                        # `.lq.FastTest.confirmNewRound`
                        # response message is not returned?
                        logger.warning(message)
                        break
                    raise InconsistentMessageError(
                        str(next_message),
                        self._browser.get_screenshot(),
                    )
                # After backfilling `ActionNewRound` into
                # the message queue,
                # the control flow is returned to the user side.
                self._message_queue_client.put_back(message)
                now = datetime.datetime.now(datetime.UTC)
                MatchPresentation._wait(self._browser, deadline - now)
                now = datetime.datetime.now(datetime.UTC)
                new_presentation = MatchPresentation(
                    self._browser,
                    self._message_queue_client,
                    self._creator,
                    self._prev_presentation,
                    deadline - now,
                    match_state=self._match_state,
                )
                self._set_new_presentation(new_presentation)
                return

            if name == ".lq.NotifyGameEndResult":
                # At the end of the game
                logger.info(message)
                # TODO: Processing message content
                template = Template.open_file(
                    "template/match/match_result_confirm",
                    self._browser.zoom_ratio,
                )
                template.wait_until_then_click(self._browser, deadline)
                self._on_end_of_match(deadline)
                return

            raise InconsistentMessageError(
                str(message),
                self._browser.get_screenshot(),
            )

    def _wait_impl(self, timeout: TimeoutType = 300.0) -> None:
        deadline = timeout_to_deadline(timeout)

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout"
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
            _, name, request, _, timestamp = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            if name == ".lq.ActionPrototype":
                step, action_name, data = _common.parse_action(request)
                action_info = {
                    "step": step,
                    "action_name": action_name,
                    "data": data,
                }

                if step != self._step:
                    now = datetime.datetime.now(datetime.UTC)
                    message = self._workaround_for_reordered_actions(
                        message,
                        self._step,
                        deadline - now,
                    )
                    assert message is not None
                    _, name, request, _, timestamp = message
                    assert name == ".lq.ActionPrototype"
                    step, action_name, data = _common.parse_action(request)
                    assert step == self._step
                    action_info = {
                        "step": step,
                        "action_name": action_name,
                        "data": data,
                    }
                self._step += 1

                if action_name == "ActionMJStart":
                    raise InconsistentMessageError(
                        str(action_info),
                        self._browser.get_screenshot(),
                    )

                if action_name == "ActionNewRound":
                    raise InconsistentMessageError(
                        str(action_info),
                        self._browser.get_screenshot(),
                    )

                if action_name == "ActionDealTile":
                    logger.info(action_info)
                    self._events.append(ZimoEvent(data, timestamp))
                    self._round_state._on_zimo(data)  # noqa: SLF001
                    if "operation" in data:
                        if len(data["operation"]["operation_list"]) == 0:
                            return
                        self._operation_list = OperationList(data["operation"])
                    return

                if action_name == "ActionDiscardTile":
                    logger.info(action_info)
                    self._events.append(DapaiEvent(data, timestamp))
                    self._round_state._on_dapai(data)  # noqa: SLF001
                    if "operation" in data:
                        if len(data["operation"]["operation_list"]) == 0:
                            return
                        self._operation_list = OperationList(data["operation"])
                    return

                if action_name == "ActionChiPengGang":
                    logger.info(action_info)
                    self._events.append(ChiPengGangEvent(data, timestamp))
                    self._round_state._on_chipenggang(data)  # noqa: SLF001
                    if "operation" in data:
                        if len(data["operation"]["operation_list"]) == 0:
                            return
                        self._operation_list = OperationList(data["operation"])
                    return

                if action_name == "ActionAnGangAddGang":
                    logger.info(action_info)
                    self._events.append(AngangJiagangEvent(data, timestamp))
                    self._round_state._on_angang_jiagang(data)  # noqa: SLF001
                    if "operation" in data:
                        if len(data["operation"]["operation_list"]) == 0:
                            return
                        self._operation_list = OperationList(data["operation"])
                    return

                if action_name == "ActionBaBei":
                    logger.info(action_info)
                    self._events.append(BabeiEvent(data, timestamp))
                    self._round_state._on_babei(data)  # noqa: SLF001
                    if "operation" in data:
                        if len(data["operation"]["operation_list"]) == 0:
                            return
                        self._operation_list = OperationList(data["operation"])
                    return

                if action_name == "ActionHule":
                    logger.info(action_info)
                    self._events.append(HuleEvent(data, timestamp))

                    template = Template.open_file(
                        "template/match/hule_confirm",
                        self._browser.zoom_ratio,
                    )
                    click_count = 0
                    while True:
                        if datetime.datetime.now(datetime.UTC) > deadline:
                            msg = "Timeout."
                            raise PresentationTimeoutError(
                                msg,
                                self._browser.get_screenshot(),
                            )

                        # Click the "Confirm" button on
                        # the winning screen. However, there are cases
                        # where the winning screen is skipped and the
                        # next game starts suddenly, so we will take
                        # a workaround to deal with this phenomenon.
                        if template.click_if_match(self._browser):
                            click_count += 1
                            if click_count == len(data["hules"]):
                                break
                            continue

                        message1 = self._message_queue_client.dequeue_message(
                            0.1,
                        )
                        if message1 is None:
                            continue
                        _, name1, _, _, _ = message1

                        if name1 in MatchPresentation._COMMON_MESSAGE_NAMES:
                            self._on_common_message(message1)
                            continue

                        if name1 == ".lq.FastTest.inputOperation":
                            # If the response message for the zimohu
                            # selection comes after `ActionHule`
                            logger.info(message1)
                            continue

                        if name1 == ".lq.FastTest.inputChiPengGang":
                            # If the other player's hule is given
                            # priority over the home's Chi Peng Kang
                            # selection, and the response message of
                            # `.lq.FastTest.inputChiPengGang` comes
                            # after `ActionHule`.
                            logger.info(message1)
                            continue

                        if name1 == ".lq.NotifyGameEndResult":
                            # If you receive the
                            # `.lq.NotifyGameEndResult` message
                            # before clicking the "Confirm" button
                            # on the winning screen
                            # Backfill prefetched messages.
                            self._message_queue_client.put_back(message1)
                            continue

                        if name1 == ".lq.ActionPrototype":
                            # If the winning screen is skipped
                            # and the next game starts
                            # Backfill prefetched messages.
                            self._message_queue_client.put_back(message1)
                            break

                        # If `.lq.FastTest.confirmNewRound`
                        # is being exchanged, there is a high
                        # possibility that the screen drawing
                        # is incorrect, so request that
                        # the browser be reloaded.
                        if name1 == ".lq.FastTest.confirmNewRound":
                            logger.warning(message1)
                            msg = "Request to refresh the browser."
                            raise BrowserRefreshRequest(
                                msg,
                                self._browser,
                                self._browser.get_screenshot(),
                            )

                        raise InconsistentMessageError(str(message1))

                    self._on_end_of_round(deadline)
                    return

                if action_name == "ActionNoTile":
                    logger.info(action_info)
                    self._events.append(NoTileEvent(data, timestamp))

                    template = Template.open_file(
                        "template/match/no_tile_confirm",
                        self._browser.zoom_ratio,
                    )
                    template.wait_until_then_click(self._browser, deadline)

                    if data["liujumanguan"]:
                        # If there is someone who has achieved
                        # Liujumanguan, there will be the same effect
                        # as hule, so you will need to click the
                        # "Confirm" button for it.
                        template = Template.open_file(
                            "template/match/hule_confirm",
                            self._browser.zoom_ratio,
                        )
                        for _ in range(len(data["scores"])):
                            template.wait_until_then_click(
                                self._browser,
                                deadline,
                            )

                    self._on_end_of_round(deadline)
                    return

                if action_name == "ActionLiuJu":
                    logger.info(action_info)
                    self._events.append(LiujuEvent(data, timestamp))

                    self._on_end_of_round(deadline)
                    return

            if name == ".lq.FastTest.inputOperation":
                logger.info(message)
                continue

            if name == ".lq.FastTest.inputChiPengGang":
                logger.info(message)
                continue

            if name == ".lq.FastTest.syncGame":
                logger.warning(message)
                self._on_sync_game(message, restore=False)
                return

            if name == ".lq.FastTest.finishSyncGame":
                logger.warning(message)
                return

            raise InconsistentMessageError(
                str(message),
                self._browser.get_screenshot(),
            )

    def wait(self, timeout: TimeoutType = 300.0) -> None:
        self._assert_not_stale()

        if self._operation_list is not None:
            msg = "Must select an operation."
            raise InvalidOperationError(msg, self._browser.get_screenshot())
        self._wait_impl(timeout)

    def _dapai(self, index: int, forbidden_tiles: list[str]) -> None:
        if index is None:
            msg = "Must specify an index for dapai."
            raise InvalidOperationError(msg, self._browser.get_screenshot())
        num_tiles = len(self._round_state.shoupai)
        num_tiles += 0 if (self._round_state.zimopai is None) else 1
        if index >= num_tiles:
            msg = "Out of index for dapai."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        if (self.zimopai is None) and (self.shoupai[index] in forbidden_tiles):
            # Validate that you are not trying to discard a tile
            # that cannot be swap-calling immediately after fulu.
            msg = "An invalid operation: Swap-Calling."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        if (self.zimopai is not None) and index == num_tiles - 1:
            # Moqie
            match index:
                case 13:
                    left = 1487
                case 10:
                    left = 1203
                case 7:
                    left = 918
                case 4:
                    left = 633
                case 1:
                    left = 348
                case _:
                    raise AssertionError
        else:
            # Discard from hand
            # Coordinates of hand
            left = int(224 + index * 94.91)

        top = 922
        height = 149
        width = 89

        # Click 10% inside the tile because you can touch
        # the adjacent tile at the very edge of the tile.
        left += int(width * 0.1)
        top += int(height * 0.1)
        width = int(width * 0.8)
        # Clicking fails with `height * 0.8`.
        height = int(height * 0.7)

        left = int(left * self._browser.zoom_ratio)
        top = int(top * self._browser.zoom_ratio)
        width = int(width * self._browser.zoom_ratio)
        height = int(height * self._browser.zoom_ratio)

        # Clicking won't discard a tile unless it position the mouse
        # cursor over it in advance.
        self._browser.move_to_region(left, top, width, height, edge_sigma=1.0)
        time.sleep(0.04)

        # `timeout=5.0` may be too short
        # when the screen display freezes.
        self._robust_click_region(
            left,
            top,
            width,
            height,
            interval=1.0,
            timeout=25.0,
            edge_sigma=1.0,
        )

        # If the mouse cursor is placed over the tiles in the hand,
        # winning tile candidates may be displayed and interfere with
        # template matching. Therefore, move the mouse cursor to an
        # appropriate position where there are no tiles in the hand.
        self._browser.move_to_region(
            int(986 * self._browser.zoom_ratio),
            int(806 * self._browser.zoom_ratio),
            int(134 * self._browser.zoom_ratio),
            int(57 * self._browser.zoom_ratio),
            edge_sigma=1.0,
        )

    def select_operation(
        self,
        operation: OperationBase | None,
        index: int | None = None,
        timeout: TimeoutType = 300.0,
    ) -> None:
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        if self._operation_list is None:
            msg = "No operation exists for now."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        if operation is not None:
            operation_exists = False
            operation_type = type(operation)
            for op in self._operation_list:
                if isinstance(op, operation_type):
                    operation = op
                    operation_exists = True
                    break
            if not operation_exists:
                msg = "An invalid operation."
                raise InvalidOperationError(
                    msg,
                    self._browser.get_screenshot(),
                )

        match operation:
            case None:
                self._skip_operation(deadline)
            case DapaiOperation():
                # Dapai
                if self.ju == self.seat and self.first_draw:
                    # When you are the parent, the tiles are moving
                    # due to the effect of the tile deal, so if you
                    # don't wait until the effect ends before playing
                    # the tiles, you may end up clicking on an
                    # unintended tile and discarding it.
                    time.sleep(2.0)
                if index is None:
                    msg = "Index not specified."
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
                self._dapai(index, operation.forbidden_tiles)
            case ChiOperation():
                self._operate_chi(operation, index, deadline)
            case PengOperation():
                self._operate_peng(operation, index, deadline)
            case AngangOperation():
                self._operate_angang(operation)
            case DaminggangOperation():
                self._operate_daminggang(operation, deadline)
            case JiagangOperation():
                self._operate_jiagang(operation, index)
            case LiqiOperation():
                if index is None:
                    msg = "Index not specified."
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
                self._operate_liqi(operation, index)
            case ZimohuOperation():
                self._operate_hu(deadline)
                return
            case RongOperation():
                self._operate_hu(deadline)
                return
            case JiuzhongjiupaiOperation():
                self._operate_jiuzhongjiupai()
            case BabeiOperation():
                self._operate_babei()
            case _:
                msg = (
                    "An invalid operation.\n"
                    f"operation: {operation}\n"
                    f"index: {index}"
                )
                raise InvalidOperationError(
                    msg,
                    self._browser.get_screenshot(),
                )

        self._operation_list = None
        now = datetime.datetime.now(datetime.UTC)
        self._wait_impl(deadline - now)
        return

    def _skip_operation(self, deadline: datetime.datetime) -> None:
        # Skip options. Skip's UI interaction with her needs
        # to be done as quickly as possible to avoid lag reading.
        # Therefore, if you want to skip Chi Peng Gang Rong
        # against another player's tiles, you can do so by
        # clicking the "No Chii/Pon/Kan" button
        # (Clicking the "No Chii/Pon/Kan" button even after
        # the options appear has the same effect as clicking
        # the "Skip" button.). Once the skip is complete,
        # click the "No Chii/Pon/Kan" button again to return
        # to the state where the you can fulu.
        if self._round_state is None:
            msg = "Round state is not initialized."
            raise RuntimeError(msg)

        should_click_skip: bool = False
        if self._round_state.liqi[self.seat]:
            should_click_skip = True
        elif self._operation_list is not None:
            for op in self._operation_list:
                if isinstance(op, ZimohuOperation | RongOperation):
                    should_click_skip = True
                    break

        if should_click_skip:
            self._skip_by_skip_button(deadline)
        else:
            self._skip_by_no_melding(deadline)

    def _skip_by_skip_button(self, deadline: datetime.datetime) -> None:
        template = Template.open_file(
            "template/match/skip",
            self._browser.zoom_ratio,
        )
        try:
            # If you do not set the `timeout` to a short value,
            # you will not be able to respond to the hule screen
            # when you are interrupted by Rong from other player.
            template.wait_for_then_click(self._browser, timeout=5.0)
        except PresentationTimeoutError as e:
            # Possibly interfered with by Chi, Peng, Gang, or Rong
            # from other player.
            while True:
                now = datetime.datetime.now(datetime.UTC)
                message = self._message_queue_client.dequeue_message(
                    deadline - now,
                )
                if message is None:
                    msg = (
                        "The WebSocket message that "
                        "was supposed to be present is missing."
                    )
                    raise UnexpectedStateError(
                        msg,
                        self._browser.get_screenshot(),
                    ) from e
                _, name, request, _, _ = message
                if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                    self._on_common_message(message)
                    continue
                if name == ".lq.ActionPrototype":
                    _, action_name, _ = _common.parse_action(request)
                    if action_name in ("ActionChiPengGang", "ActionHule"):
                        # You were being disturbed by
                        # Chi, Peng, Gang, or Rong from other player.
                        # Backfill prefetched messages.
                        self._message_queue_client.put_back(message)
                        self._operation_list = None
                        now = datetime.datetime.now(datetime.UTC)
                        self._wait_impl(deadline - now)
                        return
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputOperation":
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputChiPengGang":
                    # It is highly likely that the drawing on
                    # the screen is distorted and the "Skip" button
                    # cannot be clicked. Therefore, it is
                    # recommended to refresh the browser.
                    msg = "A rendering problem may occur."
                    raise BrowserRefreshRequest(
                        msg,
                        self._browser,
                        self._browser.get_screenshot(),
                    ) from e
                raise InconsistentMessageError(
                    str(message),
                    self._browser.get_screenshot(),
                ) from e

    def _skip_by_no_melding(self, deadline: datetime.datetime) -> None:
        left = int(18 * self._browser.zoom_ratio)
        top = int(625 * self._browser.zoom_ratio)
        width = int(40 * self._browser.zoom_ratio)
        height = int(40 * self._browser.zoom_ratio)
        self._browser.click_region(left, top, width, height, edge_sigma=1.0)

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout"
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
            _, name, _, _, _ = message
            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue
            if name == ".lq.FastTest.inputOperation":
                raise InconsistentMessageError(
                    str(message),
                    self._browser.get_screenshot(),
                )
            if name == ".lq.FastTest.inputChiPengGang":
                break
            if name == ".lq.ActionPrototype":
                break

        # Backfill prefetched messages.
        self._message_queue_client.put_back(message)

        self._browser.click_region(left, top, width, height, edge_sigma=1.0)

    def _operate_chi(
        self,
        operation: ChiOperation,
        index: int | None,
        deadline: datetime.datetime,
    ) -> None:
        template = Template.open_file(
            "template/match/chi",
            self._browser.zoom_ratio,
        )
        try:
            # If you do not set the `timeout` to a short value,
            # you will not be able to respond to the hule screen
            # when you are interrupted by Rong from other player.
            template.wait_for_then_click(self._browser, timeout=5.0)
        except PresentationTimeoutError as e:
            # Possibly interfered with by Peng, Gang, or Rong
            # from other player.
            while True:
                now = datetime.datetime.now(datetime.UTC)
                message = self._message_queue_client.dequeue_message(
                    deadline - now,
                )
                if message is None:
                    msg = (
                        "The WebSocket message that "
                        "was supposed to be present is missing."
                    )
                    raise UnexpectedStateError(
                        msg,
                        self._browser.get_screenshot(),
                    ) from e
                _, name, request, _, _ = message
                if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                    self._on_common_message(message)
                    continue
                if name == ".lq.ActionPrototype":
                    _, action_name, _ = _common.parse_action(request)
                    if action_name in ("ActionChiPengGang", "ActionHule"):
                        # You were being disturbed by
                        # Peng, Gang, or Rong from other player.
                        # Backfill prefetched messages.
                        self._message_queue_client.put_back(message)
                        self._operation_list = None
                        now = datetime.datetime.now(datetime.UTC)
                        self._wait_impl(deadline - now)
                        return
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputOperation":
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputChiPengGang":
                    # It is highly likely that the drawing on
                    # the screen is distorted and the "Chi" button
                    # cannot be clicked. Therefore, it is
                    # recommended to refresh the browser.
                    msg = "A rendering problem may occur."
                    raise BrowserRefreshRequest(
                        msg,
                        self._browser,
                        self._browser.get_screenshot(),
                    ) from e
                raise InconsistentMessageError(
                    str(message),
                    self._browser.get_screenshot(),
                ) from e

        if (num_combinations := len(operation.combinations)) >= 2:
            if index is None:
                msg = "Must specify an index."
                raise InvalidOperationError(
                    msg,
                    self._browser.get_screenshot(),
                )

            if num_combinations == 2:
                if index == 0:
                    left = 761
                elif index == 1:
                    left = 961
                else:
                    msg = f"{index}: out-of-range index"
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
            elif num_combinations == 3:
                if index == 0:
                    left = 661
                elif index == 1:
                    left = 861
                elif index == 2:
                    left = 1061
                else:
                    msg = f"{index}: out-of-range index"
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
            elif num_combinations == 4:
                if index == 0:
                    left = 561
                elif index == 1:
                    left = 761
                elif index == 2:
                    left = 961
                elif index == 3:
                    left = 1161
                else:
                    msg = f"{index}: out-of-range index"
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
            elif num_combinations == 5:
                if index == 0:
                    left = 461
                elif index == 1:
                    left = 661
                elif index == 2:
                    left = 861
                elif index == 3:
                    left = 1061
                elif index == 4:
                    left = 1261
                else:
                    msg = f"{index}: out-of-range index"
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
            else:
                msg = (
                    f"There are {num_combinations} "
                    "combinations that can be Chi."
                )
                raise UnexpectedStateError(msg, self._browser.get_screenshot())

            left = int(left * self._browser.zoom_ratio)
            top = int(692 * self._browser.zoom_ratio)
            width = int(157 * self._browser.zoom_ratio)
            height = int(117 * self._browser.zoom_ratio)

            time.sleep(0.4)
            self._browser.click_region(left, top, width, height)

        # Some of the tiles in your hand may slide right
        # after the Chi, so if you don't add a wait time for
        # the slide to finish, you may click on an unintended tile
        # when selecting a discarded tile.
        time.sleep(1.0)

    def _operate_peng(
        self,
        operation: PengOperation,
        index: int | None,
        deadline: datetime.datetime,
    ) -> None:
        template = Template.open_file(
            "template/match/peng",
            self._browser.zoom_ratio,
        )
        try:
            # If you do not set the `timeout` to a short value,
            # you will not be able to respond to the hule screen
            # when you are interrupted by Rong from other player.
            template.wait_for_then_click(self._browser, timeout=5.0)
        except PresentationTimeoutError as e:
            # Possibly interfered with by Rong from other player.
            while True:
                now = datetime.datetime.now(datetime.UTC)
                message = self._message_queue_client.dequeue_message(
                    deadline - now,
                )
                if message is None:
                    msg = (
                        "The WebSocket message that "
                        "was supposed to be present is missing."
                    )
                    raise UnexpectedStateError(
                        msg,
                        self._browser.get_screenshot(),
                    ) from e
                _, name, request, _, _ = message
                if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                    self._on_common_message(message)
                    continue
                if name == ".lq.ActionPrototype":
                    _, action_name, _ = _common.parse_action(request)
                    if action_name == "ActionHule":
                        # You were being disturbed by
                        # Rong from other player.
                        # Backfill prefetched messages.
                        self._message_queue_client.put_back(message)
                        self._operation_list = None
                        now = datetime.datetime.now(datetime.UTC)
                        self._wait_impl(deadline - now)
                        return
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputOperation":
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputChiPengGang":
                    # It is highly likely that the drawing on
                    # the screen is distorted and the "Peng" button
                    # cannot be clicked. Therefore, it is
                    # recommended to refresh the browser.
                    msg = "A rendering problem may occur."
                    raise BrowserRefreshRequest(
                        msg,
                        self._browser,
                        self._browser.get_screenshot(),
                    ) from e
                raise InconsistentMessageError(
                    str(message),
                    self._browser.get_screenshot(),
                ) from e

        if (num_combinations := len(operation.combinations)) >= 2:
            if index is None:
                msg = "Must specify an index."
                raise InvalidOperationError(
                    msg,
                    self._browser.get_screenshot(),
                )

            if num_combinations == 2:
                if index == 0:
                    left = 761
                elif index == 1:
                    left = 961
                else:
                    msg = f"{index}: out-of-range index"
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
            else:
                msg = (
                    f"There are {num_combinations} "
                    "combinations that can be Peng."
                )
                raise UnexpectedStateError(msg, self._browser.get_screenshot())

            left = int(left * self._browser.zoom_ratio)
            top = int(692 * self._browser.zoom_ratio)
            width = int(157 * self._browser.zoom_ratio)
            height = int(117 * self._browser.zoom_ratio)

            time.sleep(0.4)
            self._browser.click_region(left, top, width, height)

        # Some of the tiles in your hand may slide right
        # after the Peng, so if you don't add a wait time for
        # the slide to finish, you may click on an unintended tile
        # when selecting a discarded tile.
        time.sleep(1.0)

    def _operate_angang(self, operation: AngangOperation) -> None:
        template = Template.open_file(
            "template/match/gang",
            self._browser.zoom_ratio,
        )
        try:
            template.wait_for_then_click(self._browser, timeout=10.0)
        except PresentationTimeoutError as e:
            msg = (
                "Rare situation encountered: "
                "Failed to click 'Gang' when AnGang. "
                "Please cooperate by providing a screenshot of the error. "
                "Thank you for your cooperation."
            )
            ss = self._browser.get_screenshot()
            rare_error = UnexpectedStateError(msg, ss)
            rare_error.save_screenshot()
            raise rare_error from e

        if (num_combinations := len(operation.combinations)) >= 2:
            if num_combinations in (2, 3):
                msg = (
                    "Not implemented operation: "
                    "AnGang when there are 2 or 3 combinations."
                    "Please cooperate by providing a screenshot of the error. "
                    "Thank you for your cooperation."
                )
                ss = self._browser.get_screenshot()
                error = NotImplementedOperationError(msg, ss)
                error.save_screenshot()
                raise error

            msg = (
                f"There are {num_combinations} "
                "combinations that can be AnGang."
            )
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Some of the tiles in your hand may slide right
        # after the Angang, so if you don't add a wait time for
        # the slide to finish, you may click on an unintended tile
        # when selecting a discarded tile.
        time.sleep(1.0)

    def _operate_daminggang(
        self,
        operation: DaminggangOperation,
        deadline: datetime.datetime,
    ) -> None:
        template = Template.open_file(
            "template/match/gang",
            self._browser.zoom_ratio,
        )
        try:
            # If you do not set the `timeout` to a short value,
            # you will not be able to respond to the hule screen
            # when you are interrupted by Rong from other player.
            template.wait_for_then_click(self._browser, timeout=5.0)
        except PresentationTimeoutError as e:
            # Possibly interfered with by Rong from other player.
            while True:
                now = datetime.datetime.now(datetime.UTC)
                message = self._message_queue_client.dequeue_message(
                    deadline - now,
                )
                if message is None:
                    msg = (
                        "The WebSocket message that "
                        "was supposed to be present is missing."
                    )
                    raise UnexpectedStateError(
                        msg,
                        self._browser.get_screenshot(),
                    ) from e
                _, name, request, _, _ = message
                if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                    self._on_common_message(message)
                    continue
                if name == ".lq.ActionPrototype":
                    _, action_name, _ = _common.parse_action(request)
                    if action_name == "ActionHule":
                        # You were being disturbed by
                        # Rong from other player.
                        # Backfill prefetched messages.
                        self._message_queue_client.put_back(message)
                        self._operation_list = None
                        now = datetime.datetime.now(datetime.UTC)
                        self._wait_impl(deadline - now)
                        return
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputOperation":
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    ) from e
                if name == ".lq.FastTest.inputChiPengGang":
                    # It is highly likely that the drawing on
                    # the screen is distorted and the "Gang" button
                    # cannot be clicked. Therefore, it is
                    # recommended to refresh the browser.
                    msg = "A rendering problem may occur."
                    raise BrowserRefreshRequest(
                        msg,
                        self._browser,
                        self._browser.get_screenshot(),
                    ) from e
                raise InconsistentMessageError(
                    str(message),
                    self._browser.get_screenshot(),
                ) from e

        if len(operation.combinations) >= 2:
            msg = (
                f"There are {len(operation.combinations)} "
                "combinations that can be DamingGang."
            )
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Some of the tiles in your hand may slide right
        # after the Damingang, so if you don't add a wait time for
        # the slide to finish, you may click on an unintended tile
        # when selecting a discarded tile.
        time.sleep(1.0)

    def _operate_jiagang(
        self,
        operation: JiagangOperation,
        index: int | None,
    ) -> None:
        template = Template.open_file(
            "template/match/gang",
            self._browser.zoom_ratio,
        )
        try:
            template.wait_for_then_click(self._browser, timeout=10.0)
        except PresentationTimeoutError as e:
            msg = (
                "Rare situation encountered: "
                "Failed to click 'Gang' when JiaGang. "
                "Please cooperate by providing a screenshot of the error. "
                "Thank you for your cooperation."
            )
            ss = self._browser.get_screenshot()
            rare_error = UnexpectedStateError(msg, ss)
            rare_error.save_screenshot()
            raise rare_error from e

        if (num_combinations := len(operation.combinations)) >= 2:
            if index is None:
                msg = "Must specify an index."
                raise InvalidOperationError(
                    msg,
                    self._browser.get_screenshot(),
                )

            if num_combinations == 2:
                if index == 0:
                    left = 601
                elif index == 1:
                    left = 961
                else:
                    msg = f"{index}: out-of-range index"
                    raise InvalidOperationError(
                        msg,
                        self._browser.get_screenshot(),
                    )
            elif num_combinations == 3:
                msg = (
                    "Not implemented operation: "
                    "Jiagang when there are 3 possible combinations."
                    "Please cooperate by providing a screenshot of the error. "
                    "Thank you for your cooperation."
                )
                ss = self._browser.get_screenshot()
                error = NotImplementedOperationError(msg, ss)
                error.save_screenshot()
                raise error
            else:
                msg = (
                    f"There are {num_combinations} "
                    "combinations that can be JiaGang."
                )
                raise UnexpectedStateError(msg, self._browser.get_screenshot())

            left = int(left * self._browser.zoom_ratio)
            top = int(692 * self._browser.zoom_ratio)
            width = int(317 * self._browser.zoom_ratio)
            height = int(117 * self._browser.zoom_ratio)

            time.sleep(0.4)
            self._browser.click_region(left, top, width, height)

        # Some of the tiles in your hand may slide right
        # after the Jiagang, so if you don't add a wait time for
        # the slide to finish, you may click on an unintended tile
        # when selecting a discarded tile.
        time.sleep(1.0)

    def _operate_liqi(self, operation: LiqiOperation, index: int) -> None:
        template = Template.open_file(
            "template/match/lizhi",
            self._browser.zoom_ratio,
        )
        try:
            template.wait_for_then_click(self._browser, timeout=5.0)
        except PresentationTimeoutError as e:
            # It is highly likely that the drawing on
            # the screen is distorted and the "Lizhi" button
            # cannot be clicked. Therefore, it is
            # recommended to refresh the browser.
            msg = "A rendering problem may occur."
            raise BrowserRefreshRequest(
                msg,
                self._browser,
                self._browser.get_screenshot(),
            ) from e

        if self.zimopai is None:
            msg = "liqi without zimopai"
            raise InvalidOperationError(
                msg,
                self._browser.get_screenshot(),
            )

        # Note that only red dora appear in the candidate_dapai_list
        # When 5{m,p,s} and the corresponding red dora are in the hand.
        deaka_candidate_dapai_list = [
            _common.normalize_akadora(tile)
            for tile in operation.candidate_dapai_list
        ]
        if (
            index < len(self.shoupai)
            and _common.normalize_akadora(self.shoupai[index])
            not in deaka_candidate_dapai_list
        ) or (
            index == len(self.shoupai)
            and _common.normalize_akadora(self.zimopai)
            not in deaka_candidate_dapai_list
        ):
            raise InvalidOperationError(
                str(index),
                self._browser.get_screenshot(),
            )

        if index > len(self.shoupai):
            msg = f"{index}: out-of-range index"
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        time.sleep(0.4)
        self._dapai(index, [])

    def _operate_hu(self, deadline: datetime.datetime) -> None:
        # Hu. To prevent slowrolling Hu, UI operations for
        # Hu must be performed in the shortest possible time.
        # Therefore, skip it by clicking the "Auto Call Win" button
        # (even after the option of Zimohu or Ronghu appears,
        # clicking the "Auto Call Win" button has the same effect
        # as clicking the "Zimo" or "Rong" button)
        left = int(18 * self._browser.zoom_ratio)
        top = int(557 * self._browser.zoom_ratio)
        width = int(40 * self._browser.zoom_ratio)
        height = int(40 * self._browser.zoom_ratio)
        self._browser.click_region(left, top, width, height, edge_sigma=1.0)
        self._operation_list = None
        now = datetime.datetime.now(datetime.UTC)
        self._wait_impl(deadline - now)

    def _operate_jiuzhongjiupai(self) -> None:
        template = Template.open_file(
            "template/match/liuju",
            self._browser.zoom_ratio,
        )
        try:
            template.wait_for_then_click(self._browser, timeout=5.0)
        except PresentationTimeoutError as e:
            # It is highly likely that the drawing on
            # the screen is distorted and the "Liuju" button
            # cannot be clicked. Therefore, it is
            # recommended to refresh the browser.
            msg = "A rendering problem may occur."
            raise BrowserRefreshRequest(
                msg,
                self._browser,
                self._browser.get_screenshot(),
            ) from e

    def _operate_babei(self) -> None:
        template = Template.open_file(
            "template/match/babei",
            self._browser.zoom_ratio,
        )
        try:
            template.wait_for_then_click(self._browser, timeout=10.0)
        except PresentationTimeoutError as e:
            # It is highly likely that the drawing on
            # the screen is distorted and the "Babei" button
            # cannot be clicked. Therefore, it is
            # recommended to refresh the browser.
            msg = "A rendering problem may occur."
            raise BrowserRefreshRequest(
                msg,
                self._browser,
                self._browser.get_screenshot(),
            ) from e

        # Some of the tiles in your hand may slide right
        # after the Babei, so if you don't add a wait time for
        # the slide to finish, you may click on an unintended tile
        # when selecting a discarded tile.
        time.sleep(1.0)
