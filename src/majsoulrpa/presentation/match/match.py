# ruff: noqa: C901, PLR0911, PLR0912, PLR0913, PLR0915, PLR2004, S101
import datetime
import time
from logging import getLogger

import cv2

from majsoulrpa import common
from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase, Message
from majsoulrpa._impl.template import Template, screenshot_to_opencv
from majsoulrpa.common import TimeoutType
from majsoulrpa.presentation.match.event import (
    AngangJiagangEvent,
    ChiPengGangEvent,
    DapaiEvent,
    HuleEvent,
    LiujuEvent,
    NewRoundEvent,
    NoTileEvent,
    ZimoEvent,
)
from majsoulrpa.presentation.match.operation import (
    AngangOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    JiagangOperation,
    JiuzhongjiupaiOperation,
    LiqiOperation,
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
    BrowserRefreshRequest,
    InconsistentMessage,
    InvalidOperation,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetected,
    Timeout,
)

from . import _common

logger = getLogger(__name__)


class MatchPresentation(PresentationBase):

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 60.0) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, browser.get_screenshot())
            templates = [f"template/match/marker{i}" for i in range(4)]
            if Template.match_one_of(
                browser.get_screenshot(), templates, browser.zoom_ratio,
            ) != -1:
                break

    _COMMON_MESSAGE_NAMES = (
        ".lq.Lobby.heatbeat",
        ".lq.Lobby.loginBeat",
        ".lq.NotifyReviveCoinUpdate",
        ".lq.NotifyGiftSendRefresh",
        ".lq.NotifyDailyTaskUpdate",
        ".lq.NotifyShopUpdate",
        ".lq.NotifyAccountChallengeTaskUpdate",
        ".lq.NotifyAccountUpdate",
        ".lq.NotifyActivityChange",
        ".lq.NotifyAnnouncementUpdate",
        ".lq.FastTest.authGame",
        ".lq.Lobby.oauth2Login",
        ".lq.FastTest.checkNetworkDelay",
        ".lq.FastTest.fetchGamePlayerState",
        ".lq.NotifyPlayerConnectionState",
        ".lq.NotifyGameBroadcast",
        ".lq.PlayerLeaving",
    )

    def _on_common_message(self, message: Message) -> None:  # noqa: PLR0911
        _, name, request, _, _ = message

        match name:
            case ".lq.Lobby.heatbeat":
                # frequently exchanged
                return
            case ".lq.Lobby.loginBeat":
                # rarely exchanged
                logger.warning(message)
                return
            case (".lq.NotifyReviveCoinUpdate"
                  | ".lq.NotifyGiftSendRefresh"
                  | ".lq.NotifyDailyTaskUpdate"
                  | ".lq.NotifyShopUpdate"
                  | ".lq.Lobby.fetchShopInterval"
                  | ".lq.NotifyAccountChallengeTaskUpdate"
                  | ".lq.NotifyAccountChallengeTaskUpdate"
                  | ".lq.NotifyAccountUpdate"
                  | ".lq.NotifyActivityChange"): # ?
                #Exchanged if the date (06:00:00 (UTC+0900)) is crossed
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
                raise InconsistentMessage(str(message))
            case ".lq.FastTest.checkNetworkDelay":
                return
            case (".lq.FastTest.fetchGamePlayerState"
                  | ".lq.NotifyPlayerConnectionState"):
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

    def __init__(
        self, browser: BrowserBase, db_client: DBClientBase,
        creator: PresentationCreatorBase,
        prev_presentation: Presentation | None,
        timeout: TimeoutType = 60.0,
        *, match_state: MatchState | None = None,
    ) -> None:
        super().__init__(browser, db_client, creator)

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        self._prev_presentation = prev_presentation
        self._step = 0
        self._events = []
        if match_state is None:
            match_state = MatchState()
        self._match_state = match_state
        self._round_state = None
        self._operation_list = None

        templates = [f"template/match/marker{i}" for i in range(4)]
        sct = browser.get_screenshot()
        if Template.match_one_of(sct, templates, browser.zoom_ratio) == -1:
            # For postmortem.
            for i in range(4):
                template = Template.open_file(f"template/match/marker{i}",
                                              browser.zoom_ratio)
                x, y, score = template.best_template_match(sct)
                print(f"({x}, {y}): score = {score}")  # noqa: T201
            now = datetime.datetime.now(datetime.UTC)
            img = screenshot_to_opencv(sct)
            cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
            msg = "Could not detect 'match_main'."
            raise PresentationNotDetected(msg, sct)

        deadline = datetime.datetime.now(datetime.UTC) + timeout

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._db_client.dequeue_message(deadline - now)
            if message is None:
                msg = "Timeout."
                raise Timeout(msg, sct)
            _, name, request, response, timestamp = message

            match name:
                case (".lq.Lobby.oauth2Auth"
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
                      | ".lq.Lobby.loginSuccess"
                      | ".lq.Lobby.fetchCharacterInfo"
                      | ".lq.Lobby.fetchAllCommonViews"
                      | ".lq.FastTest.finishSyncGame"):
                    # Only when restarting a suspended match
                    logger.info(message)
                    continue
                case ".lq.FastTest.syncGame":
                    # Only when restarting a suspended match
                    logger.info(message)
                    self._on_sync_game(message)
                    continue
                case ".lq.Lobby.modifyRoom":
                    # If an API response message regarding changing
                    # the friendly match waiting room is returned
                    # after the friendly match has started.
                    logger.info(message)
                    continue
                case (".lq.NotifyRoomPlayerUpdate"
                      | ".lq.NotifyRoomPlayerReady"):
                    # If change notification for
                    # the friendly match waiting room was sent
                    # after the friendly match has started.
                    logger.info(message)
                    continue
                case ".lq.NotifyRoomGameStart":
                    # Friendly match starts.
                    logger.info(message)
                    uuid = request["game_uuid"]
                    self._match_state._set_uuid(uuid)  # noqa: SLF001
                    continue
                case ".lq.Lobby.startRoom":
                    logger.info(message)
                    continue
                case ".lq.FastTest.authGame":
                    logger.info(message)
                    uuid = request["game_uuid"]
                    self._match_state._set_uuid(uuid)  # noqa: SLF001

                    # TODO: Check game settings

                    player_map = {}
                    for p in response["players"]:
                        account_id = p["account_id"]
                        nickname = p["nickname"]
                        level4 = common.id_to_level(p["level"]["id"])
                        level3 = common.id_to_level(p["level3"]["id"])
                        charid = p["character"]["charid"]
                        try:
                            character = common.id_to_character(charid)
                        except KeyError:
                            # キャラクタ ID が不明なキャラクタと遭遇した場合
                            logger.warning(
                                "%s: %s: charid = %s", uuid, nickname, charid,
                            )
                            character = "UNKNOWN"
                        player_map[account_id] = MatchPlayer(
                            account_id, nickname, level4, level3, character,
                        )
                    players = []
                    for i in range(4):
                        account_id = response["seat_list"][i]
                        if account_id == db_client.account_id:
                            self._match_state._set_seat(i)  # noqa: SLF001
                        if account_id == 0:
                            player = MatchPlayer(
                                0, "CPU", "初心1", "初心1", "一姫",
                            )
                            players.append(player)
                        else:
                            players.append(player_map[account_id])
                    self._match_state._set_players(players)  # noqa: SLF001
                    continue
                case ".lq.FastTest.enterGame":
                    # TODO: Resume process for interrupted matches?
                    continue
                case ".lq.NotifyPlayerLoadGameReady":
                    logger.info(message)
                    continue
                case ".lq.ActionPrototype":
                    step, action_name, data = _common.parse_action(request)
                    action_info = {
                        "step": step, "action_name": action_name, "data": data,
                    }
                    if step != self._step:
                        raise InconsistentMessage(str(action_info), sct)
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
                            self._operation_list = \
                                OperationList(data["operation"])
                        return

                    raise InconsistentMessage(action_info, sct)

            # The conditional statement regarding '.lq.FastTest.authGame'
            # must come before this conditional statement.
            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            raise InconsistentMessage(message, sct)

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
    def fulu(self) \
            -> list[list[tuple[str, int | None, int | None, list[str]]]]:
        return self._round_state.fulu

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
    def prev_dapai(self) -> int | None:
        return self._round_state.prev_dapai

    @property
    def operation_list(self) -> OperationList | None:
        return self._operation_list

    @property
    def events(self) -> list[object]:
        return self._events

    def _robust_click_region(
        self, left: int, top: int, width: int, height: int,
        interval: TimeoutType, timeout: TimeoutType, edge_sigma: float = 2.0,
    ) -> None:
        if isinstance(interval, int | float):
            interval = datetime.timedelta(seconds=interval)

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        deadline = datetime.datetime.now(datetime.UTC) + timeout
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())

            self._browser.click_region(left, top, width, height, edge_sigma)
            message = self._db_client.dequeue_message(interval)
            if message is None:
                continue
            _, name, _, _, _ = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            match name:
                case (".lq.FastTest.inputOperation"
                      | ".lq.FastTest.inputChiPengGang"
                      | ".lq.ActionPrototype"):
                    logger.info(message)
                    break

            raise InconsistentMessage(str(message),
                                      self._browser.get_screenshot())

        # Backfill the prefetched message.
        self._db_client.put_back(message)

    def _reset_to_prev_presentation(self, timeout: TimeoutType) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        # If there is an additional "confirm" button
        # such as when receiving rewards, click it.
        template = Template.open_file("template/match/match_result_confirm",
                                      self._browser.zoom_ratio)
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout"
                raise Timeout(msg, self._browser.get_screenshot())
            try:
                template.wait_for_then_click(self._browser, 5.0)
            except Timeout:
                break

        if self._prev_presentation == Presentation.ROOMOWNER:
            now = datetime.datetime.now(datetime.UTC)
            self._creator.wait(self._browser, deadline - now,
                               Presentation.ROOMOWNER)
            now = datetime.datetime.now(datetime.UTC)
            new_presentation = self._creator.create_new_presentation(
                Presentation.MATCH, Presentation.ROOMOWNER,
                self._browser, self._db_client, timeout=(deadline - now),
            )
            self._set_new_presentation(new_presentation)
            return

        # TODO: What to do when restarting a suspended match.
        # In this case, 'self._prev_presentation' is 'None'.

        raise NotImplementedError(self._prev_presentation.name)

    def _on_end_of_match(self, deadline: datetime.datetime) -> None:
        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._db_client.dequeue_message(deadline - now)
            if message is None:
                msg = "Timeout"
                raise Timeout(msg, self._browser.get_screenshot())
            direction, name, request, _, _ = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            match name:
                case ".lq.FastTest.inputChiPengGang":
                    # The response message of
                    # '.lq.FastTest.inputChiPengGang'
                    # may be returned late,
                    # so there is a workaround for this.
                    logger.info(message)
                    continue
                case ".lq.Lobby.fetchAccountInfo":
                    logger.info(message)
                    # TODO: Processing message content
                    # Only during the event?
                    continue
                    #now = datetime.datetime.now(datetime.UTC)
                    #self._reset_to_prev_presentation(deadline - now)
                    #return
                case (".lq.NotifyAccountUpdate"
                      | ".lq.NotifyGameFinishReward"
                      | ".lq.NotifyActivityReward"
                      | ".lq.NotifyActivityPoint"
                      | ".lq.NotifyLeaderboardPoint"):
                    logger.info(message)
                    # TODO: Processing message content
                    continue
                case ".lq.NotifyActivityPointV2":
                    logger.info(message)
                    # TODO: Processing message content

                    # If there are no more messages,
                    # return to the home screen
                    message = self._db_client.dequeue_message(5)
                    if message is None:
                        now = datetime.datetime.now(datetime.UTC)
                        self._reset_to_prev_presentation(deadline - now)
                        return

                    # Backfill the prefetched message and
                    # proceed to the next.
                    self._db_client.put_back(message)
                    continue
                case ".lq.Lobby.fetchRoom":
                    # Backfill the prefetched message.
                    self._db_client.put_back(message)
                    now = datetime.datetime.now(datetime.UTC)
                    self._reset_to_prev_presentation(deadline - now)
                    return

            raise InconsistentMessage(message, self._browser.get_screenshot())

    def _workaround_for_reordered_actions(
        self, message: Message, expected_step: int, timeout: TimeoutType,
    ) -> Message:
        # Since '.lq.ActionPrototype' may not come in
        # the 'step' order, read ahead the messages and
        # sort them in the 'step' order.
        if message is None:
            msg = "'message' is 'None'."
            raise ValueError(msg)
        if message[1] != ".lq.ActionPrototype":
            raise ValueError(message)

        if expected_step < 0:
            raise ValueError(expected_step)

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        messages: list[Message] = []
        while True:
            assert message is not None
            _, name, request, _, _ = message

            flag = False

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                flag = True

            if name == ".lq.ActionPrototype":
                step, action_name, data = _common.parse_action(request)
                action_info = {
                    "step": step, "action_name": action_name, "data": data,
                }
                if step < expected_step:
                    raise InconsistentMessage(action_info,
                                              self._browser.get_screenshot())
                while len(messages) <= step - expected_step:
                    messages.append(None)
                messages[step - expected_step] = message
                if messages.count(None) == 0:
                    result = messages.pop(0)
                    while len(messages) > 0:
                        message = messages.pop(-1)
                        self._db_client.put_back(message)
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
                raise InconsistentMessage(error_message,
                                          self._browser.get_screenshot())

            now = datetime.datetime.now(datetime.UTC)
            message = self._db_client.dequeue_message(deadline - now)
            if message is None:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())

    def _workaround_for_skipped_confirm_new_round(
        self, message: Message, deadline: datetime.datetime,
    ) -> None:
        # Workaround if the '.lq.FastTest.confirmNewRound'
        # interaction is skipped.
        # In this case, the next station's '.lq.ActionPrototype'
        # messages may not arrive in 'step' order,
        # so we also do a workaround to sort them in 'step' order.
        if message is None:
            msg = "'message' is 'None'."
            raise ValueError(msg)
        _, name, request, _, _ = message
        if name != ".lq.ActionPrototype":
            raise InconsistentMessage(message, self._browser.get_screenshot())

        step, action_name, _ = _common.parse_action(request)
        if step != 0:
            now = datetime.datetime.now(datetime.UTC)
            message = self._workaround_for_reordered_actions(
                message, 0, deadline - now,
            )

        assert message is not None
        _, name, request, _, _ = message
        assert name == ".lq.ActionPrototype"
        step, action_name, _ = _common.parse_action(request)
        assert step == 0
        assert action_name == "ActionNewRound"
        self._db_client.put_back(message)

        now = datetime.datetime.now(datetime.UTC)
        MatchPresentation._wait(self._browser, deadline - now)
        now = datetime.datetime.now(datetime.UTC)
        new_presentation = MatchPresentation(
            self._browser, self._db_client, self._creator,
            self._prev_presentation, deadline - now,
            match_state=self._match_state,
        )
        self._set_new_presentation(new_presentation)

    def _on_end_of_round(self, deadline: datetime.datetime) -> None:
        template = Template.open_file("template/match/round_result_confirm",
                                      self._browser.zoom_ratio)
        round_result_confirmed = False
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())

            if ((not round_result_confirmed)
                and template.match(self._browser.get_screenshot())):
                template.click(self._browser)
                round_result_confirmed = True

            now = datetime.datetime.now(datetime.UTC)
            message = self._db_client.dequeue_message(deadline - now)
            if message is None:
                continue
            _, name, request, _, _ = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            match name:
                case ".lq.FastTest.inputOperation":
                    # The response message of
                    # '.lq.FastTest.inputOperation' may be
                    # returned late, so there isa workaround for this.
                    logger.info(message)
                    continue
                case ".lq.FastTest.inputChiPengGang":
                    # The response message of
                    # '.lq.FastTest.inputChiPengGang' may be
                    # returned late, so there is a workaround for this.
                    logger.info(message)
                    continue
                case ".lq.NotifyActivityChange":
                    logger.info(message)
                    # TODO: Parsing message content
                    continue

            if name == ".lq.FastTest.confirmNewRound":
                # At the end of the game (if there is a next game)
                logger.info(message)
                while True:
                    # Wait for 'ActionNewRound' message.
                    now = datetime.datetime.now(datetime.UTC)
                    message = self._db_client.dequeue_message(deadline - now)
                    if message is None:
                        msg = "Timeout"
                        raise Timeout(msg, self._browser.get_screenshot())
                    direction, name, request, response, timestamp = message
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
                            self._db_client.put_back(message)
                            break
                        raise InconsistentMessage(
                            action_info, self._browser.get_screenshot()
                        )
                    raise InconsistentMessage(message,
                                              self._browser.get_screenshot())

                now = datetime.datetime.now(datetime.UTC)
                MatchPresentation._wait(self._browser, deadline - now)
                now = datetime.datetime.now(datetime.UTC)
                new_presentation = MatchPresentation(
                    self._browser, self._db_client, self._creator,
                    self._prev_presentation, deadline - now,
                    match_state=self._match_state,
                )
                self._set_new_presentation(new_presentation)
                return

            if name == ".lq.ActionPrototype":
                # The order of the '.lq.FastTest.confirmNewRound'
                # response message and the 'ActionNewRound'
                # message may be reversed,
                # so here is a workaround for that case.
                step, action_name, data = _common.parse_action(request)
                if action_name != "ActionNewRound":
                    raise InconsistentMessage(
                        str({
                                "step": step,
                                "action_name": action_name,
                                "data": data,
                        }),
                        self._browser.get_screenshot(),
                    )
                while True:
                    # Wait for response message of
                    # '.lq.FastTest.confirmNewRound'
                    now = datetime.datetime.now(datetime.UTC)
                    next_message = \
                        self._db_client.dequeue_message(deadline - now)
                    if next_message is None:
                        msg = "Timeout"
                        raise Timeout(msg, self._browser.get_screenshot())
                    _, next_name, _, _, _ = next_message
                    if next_name in MatchPresentation._COMMON_MESSAGE_NAMES:
                        self._on_common_message(next_message)
                        continue
                    if next_name == ".lq.ActionPrototype":
                        # The exchange between
                        # '.lq.FastTest.confirmNewRound' and
                        # 'ActionNewRound' may be skipped and
                        # '.lq.ActionPrototype' of the next game's
                        # 'step = 1' is sent, so here is a workaround
                        # for this phenomenon.
                        # Backfill the prefetched message.
                        self._db_client.put_back(next_message)
                        self._workaround_for_skipped_confirm_new_round(
                            message, deadline,
                        )
                        return
                    if next_name == ".lq.FastTest.confirmNewRound":
                        logger.info(next_name)
                        break
                    if data["ju"] == self.seat:
                        # If you are the parent of the next game.
                        # In extremely rare circumstances,
                        # is there a case where
                        # '.lq.FastTest.confirmNewRound'
                        # response message is not returned?
                        logger.warning(message)
                        break
                    raise InconsistentMessage(next_message,
                                              self._browser.get_screenshot())
                # After backfilling 'ActionNewRound' into
                # the message queue of the DB server,
                # the control flow is returned to the user side.
                self._db_client.put_back(message)
                now = datetime.datetime.now(datetime.UTC)
                MatchPresentation._wait(self._browser, deadline - now)
                now = datetime.datetime.now(datetime.UTC)
                new_presentation = MatchPresentation(
                    self._browser, self._db_client, self._creator,
                    self._prev_presentation, deadline - now,
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
                    self._browser.zoom_ratio
                )
                template.wait_until_then_click(self._browser, deadline)
                self._on_end_of_match(deadline)
                return

            raise InconsistentMessage(message, self._browser.get_screenshot())

    def _on_sync_game(self, message: Message) -> None:
        direction, name, request, response, timestamp = message
        if direction != "outbound":
            raise ValueError(message)
        if name != ".lq.FastTest.syncGame":
            raise ValueError(message)

        game_restore = response["game_restore"]

        if game_restore["game_state"] != 1:
            raise NotImplementedError(message)

        actions: list[object] = game_restore["actions"]
        if len(actions) == 0:
            raise InconsistentMessage(message)
        if len(actions) != response["step"]:
            raise InconsistentMessage(message)

        action = actions.pop(0)
        step, name, data = _common.parse_action(action, restore=True)
        if step != 0:
            raise InconsistentMessage(action)
        if name != "ActionNewRound":
            raise InconsistentMessage(action)
        self._step = 0
        self._events.clear()
        self._events.append(NewRoundEvent(data, timestamp))
        self._round_state = RoundState(self._match_state, data)
        if (("operation" in data)
                and len(data["operation"]["operation_list"]) > 0):
            self._operation_list = OperationList(data["operation"])
        else:
            self._operation_list = None
        self._step += 1

        for action in actions:
            step, name, data = _common.parse_action(action, restore=True)
            if step != self._step:
                raise InconsistentMessage(action)

            if name == "ActionDealTile":
                self._events.append(ZimoEvent(data, timestamp))
                self._round_state._on_zimo(data)  # noqa: SLF001
                if (("operation" in data)
                        and len(data["operation"]["operation_list"]) > 0):
                    self._operation_list = OperationList(data["operation"])
                else:
                    self._operation_list = None
                self._step += 1
                continue

            if name == "ActionDiscardTile":
                self._events.append(DapaiEvent(data, timestamp))
                self._round_state._on_dapai(data)  # noqa: SLF001
                if (("operation" in data)
                        and len(data["operation"]["operation_list"]) > 0):
                    self._operation_list = OperationList(data["operation"])
                else:
                    self._operation_list = None
                self._step += 1
                continue

            if name == "ActionChiPengGang":
                self._events.append(ChiPengGangEvent(data, timestamp))
                self._round_state._on_chipenggang(data)  # noqa: SLF001
                if (("operation" in data)
                        and len(data["operation"]["operation_list"]) > 0):
                    self._operation_list = OperationList(data["operation"])
                else:
                    self._operation_list = None
                self._step += 1
                continue

            if name == "ActionAnGangAddGang":
                self._events.append(AngangJiagangEvent(data, timestamp))
                self._round_state._on_angang_jiagang(data)  # noqa: SLF001
                if (("operation" in data)
                        and len(data["operation"]["operation_list"]) > 0):
                    self._operation_list = OperationList(data["operation"])
                else:
                    self._operation_list = None
                self._step += 1
                continue

            if name == "ActionHule":
                raise InconsistentMessage(action)

            if name == "ActionNoTile":
                raise InconsistentMessage(action)

            if name == "ActionLiuJu":
                raise InconsistentMessage(action)

            raise InconsistentMessage(action)

    def _wait_impl(self, timeout: TimeoutType = 300.0) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._db_client.dequeue_message(deadline - now)
            if message is None:
                msg = "Timeout"
                raise Timeout(msg, self._browser.get_screenshot())
            _, name, request, _, timestamp = message

            if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                self._on_common_message(message)
                continue

            if name == ".lq.ActionPrototype":
                step, action_name, data = _common.parse_action(request)
                action_info = {
                    "step": step, "action_name": action_name, "data": data,
                }

                if step != self._step:
                    now = datetime.datetime.now(datetime.UTC)
                    message = self._workaround_for_reordered_actions(
                        message, self._step, deadline - now,
                    )
                    assert(message is not None)
                    _, name, request, _, timestamp = message
                    assert(name == ".lq.ActionPrototype")
                    step, action_name, data = _common.parse_action(request)
                    assert(step == self._step)
                    action_info = {
                        "step": step, "action_name": action_name, "data": data,
                    }
                self._step += 1

                if action_name == "ActionMJStart":
                    raise InconsistentMessage(str(action_info),
                                              self._browser.get_screenshot())

                if action_name == "ActionNewRound":
                    raise InconsistentMessage(str(action_info),
                                              self._browser.get_screenshot())

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
                            raise Timeout(msg, self._browser.get_screenshot())

                        # Click the "Confirm" button on
                        # the winning screen. However, there are cases
                        # where the winning screen is skipped and the
                        # next game starts suddenly, so we will take
                        # a workaround to deal with this phenomenon.
                        if template.match(self._browser.get_screenshot()):
                            template.click(self._browser)
                            click_count += 1
                            if click_count == len(data["hules"]):
                                break
                            continue

                        message1 = self._db_client.dequeue_message(0.1)
                        if message1 is None:
                            continue
                        _, name1, _, _, _ = message1

                        if name1 in MatchPresentation._COMMON_MESSAGE_NAMES:
                            self._on_common_message(message1)
                            continue

                        if name1 == ".lq.FastTest.inputOperation":
                            # If the response message for the zimohu
                            # selection comes after 'ActionHule'
                            logger.info(message1)
                            continue

                        if name1 == ".lq.FastTest.inputChiPengGang":
                            # If the other player's hule is given
                            # priority over the home's Chi Peng Kang
                            # selection, and the response message of
                            # '.lq.FastTest.inputChiPengGang' comes
                            # after 'ActionHule'.
                            logger.info(message1)
                            continue

                        if name1 == ".lq.NotifyGameEndResult":
                            # If you receive the
                            # '.lq.NotifyGameEndResult' message
                            # before clicking the "Confirm" button
                            # on the winning screen
                            # Backfill prefetched messages.
                            self._db_client.put_back(message1)
                            continue

                        if name1 == ".lq.ActionPrototype":
                            # If the winning screen is skipped
                            # and the next game starts
                            # Backfill prefetched messages.
                            self._db_client.put_back(message1)
                            break

                        # If '.lq.FastTest.confirmNewRound'
                        # is being exchanged, there is a high
                        # possibility that the screen drawing
                        # is incorrect, so request that
                        # the browser be reloaded.
                        if name1 == ".lq.FastTest.confirmNewRound":
                            logger.warning(message1)
                            msg = "Request to refresh the browser."
                            raise BrowserRefreshRequest(
                                msg, self._browser,
                                self._browser.get_screenshot(),
                            )

                        raise InconsistentMessage(str(message1))

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
                                self._browser, deadline,
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
                self._on_sync_game(message)
                return

            if name == ".lq.FastTest.finishSyncGame":
                logger.warning(message)
                return

            raise InconsistentMessage(str(message),
                                      self._browser.get_screenshot())

    def wait(self, timeout: TimeoutType = 300.0) -> None:
        self._assert_not_stale()

        if self._operation_list is not None:
            msg = "Must select an operation."
            raise InvalidOperation(msg, self._browser.get_screenshot())
        self._wait_impl(timeout)

    def _dapai(self, index: int, forbidden_tiles: list[str]) -> None:
        if index is None:
            msg = "Must specify an index for dapai."
            raise InvalidOperation(msg, self._browser.get_screenshot())
        num_tiles = len(self._round_state.shoupai)
        num_tiles += 0 if (self._round_state.zimopai is None) else 1
        if index >= num_tiles:
            msg = "Out of index for dapai."
            raise InvalidOperation(msg, self._browser.get_screenshot())

        if (self.zimopai is None) and (self.shoupai[index] in forbidden_tiles):
            # Validate that you are not trying to discard a tile
            # that cannot be swap-calling immediately after fulu.
            msg = "An invalid operation: Swap-Calling."
            raise InvalidOperation(msg, self._browser.get_screenshot())

        if (self.zimopai is not None) and index == num_tiles - 1:
            # Moqie
            if index == 13:
                left = 1487
                top = 922
                width = 89
                height = 149
            elif index == 10:
                left = 1203
                top = 922
                width = 89
                height = 149
            elif index == 7:
                left = 918
                top = 922
                width = 89
                height = 149
            elif index == 4:
                left = 633
                top = 922
                width = 90
                height = 149
            elif index == 1:
                left = 224
                top = 922
                width = 89
                height = 149
            else:
                raise AssertionError
        else:
            # Discard from hand
            # Coordinates of hand
            left = round(224 + index * 94.91)
            top = 922
            width = round(312 + index * 94.91) - left + 1
            height = 149

        # Click 10% inside the tile because you can touch
        # the adjacent tile at the very edge of the tile.
        left += round(width * 0.1)
        top += round(height * 0.1)
        width = round(width * 0.8)
        # Clicking fails with 'height * 0.8'.
        height = round(height * 0.7)

        left = round(left * self._browser.zoom_ratio)
        top = round(top * self._browser.zoom_ratio)
        width = round(width * self._browser.zoom_ratio)
        height = round(height * self._browser.zoom_ratio)

        # 'timeout=5.0' may be too short
        # when the screen display freezes.
        self._robust_click_region(left, top, width, height, interval=1.0,
                                  timeout=25.0, edge_sigma=1.0)

    def select_operation(
        self, operation: object, index: int | None = None,
        timeout: TimeoutType = 300.0,
    ) -> None:
        self._assert_not_stale()

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        if self._operation_list is None:
            msg = "No operation exists for now."
            raise InvalidOperation(msg, self._browser.get_screenshot())

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
                raise InvalidOperation(msg, self._browser.get_screenshot())

        if operation is None:
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
            # TODO: To skip Zimohu/Rong, you need to click the "Skip" button.
            left = round(14 * self._browser.zoom_ratio)
            top = round(623 * self._browser.zoom_ratio)
            width = round(43 * self._browser.zoom_ratio)
            height = round(43 * self._browser.zoom_ratio)
            self._browser.click_region(left, top, width, height, edge_sigma=1)
            while True:
                now = datetime.datetime.now(datetime.UTC)
                message = self._db_client.dequeue_message(deadline - now)
                if message is None:
                    msg = "Timeout"
                    raise Timeout(msg, self._browser.get_screenshot())
                _, name, request, _, _ = message
                if name in MatchPresentation._COMMON_MESSAGE_NAMES:
                    self._on_common_message(message)
                    continue
                if name == ".lq.FastTest.inputOperation":
                    raise InconsistentMessage(str(message),
                                              self._browser.get_screenshot())
                if name == ".lq.FastTest.inputChiPengGang":
                    break
                if name == ".lq.ActionPrototype":
                    break
            # Backfill prefetched messages.
            self._db_client.put_back(message)
            self._browser.click_region(left, top, width, height, edge_sigma=1)

            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, DapaiOperation):
            # Dapai
            if self.ju == self.seat and self.first_draw:
                # When you are the parent, the tiles are moving due to
                # the effect of the tile deal, so if you do not wait
                # until the effect ends before playing the tiles,
                # you may end up clicking on an unintended tile
                # and discarding it.
                time.sleep(1.0)
            if index is None:
                msg = "Index not specified."
                raise InvalidOperation(msg, self._browser.get_screenshot())
            self._dapai(index, operation.forbidden_tiles)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, ChiOperation):
            template = Template.open_file("template/match/chi",
                                          self._browser.zoom_ratio)
            try:
                # If you do not set the 'timeout' to a short value,
                # you will not be able to respond to the hule screen
                # when you are interrupted by Rong from other player.
                template.wait_for_then_click(self._browser, timeout=5.0)
            except Timeout as e:
                # Possibly interfered with by Peng, Gang, or Rong
                # from other player.
                while True:
                    now = datetime.datetime.now(datetime.UTC)
                    message = self._db_client.dequeue_message(deadline - now)
                    if message is None:
                        ss = self._browser.get_screenshot()
                        now = datetime.datetime.now(datetime.UTC)
                        img = screenshot_to_opencv(ss)
                        cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                        raise NotImplementedError from e
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
                            self._db_client.put_back(message)
                            self._operation_list = None
                            now = datetime.datetime.now(datetime.UTC)
                            self._wait_impl(deadline - now)
                            return
                        ss = self._browser.get_screenshot()
                        now = datetime.datetime.now(datetime.UTC)
                        img = screenshot_to_opencv(ss)
                        cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                        raise InconsistentMessage(
                            str(message), self._browser.get_screenshot(),
                        ) from e
                    if name == ".lq.FastTest.inputOperation":
                        raise InconsistentMessage(
                            str(message), self._browser.get_screenshot(),
                        ) from e
                    if name == ".lq.FastTest.inputChiPengGang":
                        # It is highly likely that the drawing on
                        # the screen is distorted and the "Chi" button
                        # cannot be clicked. Therefore, it is
                        # recommended to refresh the browser.
                        msg = "A rendering problem may occur."
                        raise BrowserRefreshRequest(
                            msg, self._browser, self._browser.get_screenshot(),
                        ) from e
                    raise InconsistentMessage(
                        str(message), self._browser.get_screenshot(),
                    ) from e
            if len(operation.combinations) >= 2:
                if index is None:
                    msg = "Must specify an index."
                    raise InvalidOperation(msg, self._browser.get_screenshot())
                if len(operation.combinations) == 2:
                    if index == 0:
                        left = 780
                    elif index == 1:
                        left = 980
                    else:
                        msg = f"{index}: out-of-range index"
                        raise InvalidOperation(msg,
                                               self._browser.get_screenshot())
                elif len(operation.combinations) == 3:
                    if index == 0:
                        left = 680
                    elif index == 1:
                        left = 880
                    elif index == 2:
                        left = 1080
                    else:
                        msg = f"{index}: out-of-range index"
                        raise InvalidOperation(msg,
                                               self._browser.get_screenshot())
                elif len(operation.combinations) == 4:
                    if index == 0:
                        left = 580
                    elif index == 1:
                        left = 780
                    elif index == 2:
                        left = 980
                    elif index == 3:
                        left = 1180
                    else:
                        msg = f"{index}: out-of-range index"
                        raise InvalidOperation(msg,
                                               self._browser.get_screenshot())
                elif len(operation.combinations) == 5:
                    if index == 0:
                        left = 480
                    elif index == 1:
                        left = 680
                    elif index == 2:
                        left = 880
                    elif index == 3:
                        left = 1080
                    elif index == 4:
                        left = 1280
                    else:
                        msg = f"{index}: out-of-range index"
                        raise InvalidOperation(msg,
                                               self._browser.get_screenshot())
                else:
                    ss = self._browser.get_screenshot()
                    now = datetime.datetime.now(datetime.UTC)
                    img = screenshot_to_opencv(ss)
                    cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                    raise AssertionError(len(operation.combinations))
                left = round(left * self._browser.zoom_ratio)
                top = round(691 * self._browser.zoom_ratio)
                width = round(160 * self._browser.zoom_ratio)
                height = round(120 * self._browser.zoom_ratio)
                self._browser.click_region(left, top, width, height)
            # Some of the tiles in your hand may slide right
            # after the Chi, so if you don't add a wait time for
            # the slide to finish, you may click on an unintended tile
            # when selecting a discarded tile.
            time.sleep(1.0)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, PengOperation):
            template = Template.open_file("template/match/peng",
                                          self._browser.zoom_ratio)
            try:
                # If you do not set the 'timeout' to a short value,
                # you will not be able to respond to the hule screen
                # when you are interrupted by Rong from other player.
                template.wait_for_then_click(self._browser, timeout=5.0)
            except Timeout as e:
                # Possibly interfered with by Rong from other player.
                while True:
                    now = datetime.datetime.now(datetime.UTC)
                    message = self._db_client.dequeue_message(deadline - now)
                    if message is None:
                        ss = self._browser.get_screenshot()
                        now = datetime.datetime.now(datetime.UTC)
                        img = screenshot_to_opencv(ss)
                        cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                        raise NotImplementedError from e
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
                            self._db_client.put_back(message)
                            self._operation_list = None
                            now = datetime.datetime.now(datetime.UTC)
                            self._wait_impl(deadline - now)
                            return
                        ss = self._browser.get_screenshot()
                        now = datetime.datetime.now(datetime.UTC)
                        img = screenshot_to_opencv(ss)
                        cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                        raise InconsistentMessage(
                            str(message), self._browser.get_screenshot(),
                        ) from e
                    if name == ".lq.FastTest.inputOperation":
                        raise InconsistentMessage(
                            str(message), self._browser.get_screenshot(),
                        ) from e
                    if name == ".lq.FastTest.inputChiPengGang":
                        # It is highly likely that the drawing on
                        # the screen is distorted and the "Peng" button
                        # cannot be clicked. Therefore, it is
                        # recommended to refresh the browser.
                        msg = "A rendering problem may occur."
                        raise BrowserRefreshRequest(
                            msg, self._browser, self._browser.get_screenshot(),
                        ) from e
                    raise InconsistentMessage(
                        str(message), self._browser.get_screenshot(),
                    ) from e
            if len(operation.combinations) >= 2:
                if len(operation.combinations) == 2:
                    if index == 0:
                        left = 780
                    elif index == 1:
                        left = 980
                    else:
                        msg = f"{index}: out-of-range index"
                        raise InvalidOperation(msg,
                                               self._browser.get_screenshot())
                else:
                    ss = self._browser.get_screenshot()
                    now = datetime.datetime.now(datetime.UTC)
                    img = screenshot_to_opencv(ss)
                    cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                    raise AssertionError(len(operation.combinations))

                left = round(left * self._browser.zoom_ratio)
                top = round(691 * self._browser.zoom_ratio)
                width = round(160 * self._browser.zoom_ratio)
                height = round(120 * self._browser.zoom_ratio)
                self._browser.click_region(left, top, width, height)
            # Some of the tiles in your hand may slide right
            # after the Peng, so if you don't add a wait time for
            # the slide to finish, you may click on an unintended tile
            # when selecting a discarded tile.
            time.sleep(1.0)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, AngangOperation):
            template = Template.open_file("template/match/gang",
                                          self._browser.zoom_ratio)
            try:
                template.wait_for_then_click(self._browser, timeout=10.0)
            except Timeout as e:
                ss = self._browser.get_screenshot()
                now = datetime.datetime.now(datetime.UTC)
                img = screenshot_to_opencv(ss)
                cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                raise NotImplementedError from e

            if len(operation.combinations) >= 2:
                ss = self._browser.get_screenshot()
                now = datetime.datetime.now(datetime.UTC)
                img = screenshot_to_opencv(ss)
                cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                raise NotImplementedError
            # Some of the tiles in your hand may slide right
            # after the Angang, so if you don't add a wait time for
            # the slide to finish, you may click on an unintended tile
            # when selecting a discarded tile.
            time.sleep(1.0)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, DaminggangOperation):
            template = Template.open_file("template/match/gang",
                                          self._browser.zoom_ratio)
            try:
                template.wait_for_then_click(self._browser, timeout=10.0)
            except Timeout as e:
                # TODO: Possibly interfered with by Rong from other player.
                ss = self._browser.get_screenshot()
                now = datetime.datetime.now(datetime.UTC)
                img = screenshot_to_opencv(ss)
                cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                raise NotImplementedError from e

            if len(operation.combinations) >= 2:
                ss = self._browser.get_screenshot()
                now = datetime.datetime.now(datetime.UTC)
                img = screenshot_to_opencv(ss)
                cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                raise NotImplementedError
            # Some of the tiles in your hand may slide right
            # after the Damingang, so if you don't add a wait time for
            # the slide to finish, you may click on an unintended tile
            # when selecting a discarded tile.
            time.sleep(1.0)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, JiagangOperation):
            template = Template.open_file("template/match/gang",
                                          self._browser.zoom_ratio)
            try:
                template.wait_for_then_click(self._browser, timeout=10.0)
            except Timeout as e:
                ss = self._browser.get_screenshot()
                now = datetime.datetime.now(datetime.UTC)
                img = screenshot_to_opencv(ss)
                cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                raise NotImplementedError from e

            if len(operation.combinations) >= 2:
                if len(operation.combinations) == 2:
                    if index == 0:
                        left = 600
                    elif index == 1:
                        left = 960
                    else:
                        msg = f"{index}: out-of-range index"
                        raise InvalidOperation(msg,
                                               self._browser.get_screenshot())
                else:
                    ss = self._browser.get_screenshot()
                    now = datetime.datetime.now(datetime.UTC)
                    img = screenshot_to_opencv(ss)
                    cv2.imwrite(now.strftime("%Y-%m-%d-%H-%M-%S.png"), img)
                    raise NotImplementedError

                left = round(left * self._browser.zoom_ratio)
                top = round(691 * self._browser.zoom_ratio)
                width = round(320 * self._browser.zoom_ratio)
                height = round(120 * self._browser.zoom_ratio)
                self._browser.click_region(left, top, width, height)
            # Some of the tiles in your hand may slide right
            # after the Jiagang, so if you don't add a wait time for
            # the slide to finish, you may click on an unintended tile
            # when selecting a discarded tile.
            time.sleep(1.0)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, LiqiOperation):
            template = Template.open_file("template/match/lizhi",
                                          self._browser.zoom_ratio)
            try:
                template.wait_for_then_click(self._browser, timeout=5.0)
            except Timeout as e:
                # It is highly likely that the drawing on
                # the screen is distorted and the "Lizhi" button
                # cannot be clicked. Therefore, it is
                # recommended to refresh the browser.
                msg = "A rendering problem may occur."
                raise BrowserRefreshRequest(
                    msg, self._browser, self._browser.get_screenshot(),
                ) from e

            if index < len(self.shoupai):
                if self.shoupai[index] not in operation.candidate_dapai_list:
                    raise InvalidOperation(str(index),
                                           self._browser.get_screenshot())
            elif index == len(self.shoupai):
                if self.zimopai not in operation.candidate_dapai_list:
                    msg = ""
                    raise InvalidOperation(msg, self._browser.get_screenshot())
            else:
                msg = f"{index}: out-of-range index"
                raise InvalidOperation(msg, self._browser.get_screenshot())
            self._dapai(index, [])
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, ZimohuOperation):
            # Zimohu. To prevent slowrolling Zimo, UI operations for
            # Zimohu must be performed in the shortest possible time.
            # Therefore, skip it by clicking the "Auto Call Win" button
            # (even after the option of Zimohu appears,
            # clicking the "Auto Call Win" button has the same effect
            # as clicking the "Zimo" button)
            left = round(14 * self._browser.zoom_ratio)
            top = round(557 * self._browser.zoom_ratio)
            width = round(43 * self._browser.zoom_ratio)
            height = round(43 * self._browser.zoom_ratio)
            self._browser.click_region(left, top, width, height, edge_sigma=1)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, RongOperation):
            # Ronghu. To prevent slowrolling Rong, UI operations for
            # Ronghu must be performed in the shortest possible time.
            # Therefore, skip it by clicking the "Auto Call Win" button
            # (even after the option of Ronghu appears,
            # clicking the "Auto Call Win" button has the same effect
            # as clicking the "Rong" button)
            left = round(14 * self._browser.zoom_ratio)
            top = round(557 * self._browser.zoom_ratio)
            width = round(43 * self._browser.zoom_ratio)
            height = round(43 * self._browser.zoom_ratio)
            self._browser.click_region(left, top, width, height, edge_sigma=1)
            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        if isinstance(operation, JiuzhongjiupaiOperation):
            template = Template.open_file("template/match/liuju",
                                          self._browser.zoom_ratio)
            try:
                template.wait_for_then_click(self._browser, timeout=5.0)
            except Timeout as e:
                # It is highly likely that the drawing on
                # the screen is distorted and the "Liuju" button
                # cannot be clicked. Therefore, it is
                # recommended to refresh the browser.
                msg = "A rendering problem may occur."
                raise BrowserRefreshRequest(
                    msg, self._browser, self._browser.get_screenshot(),
                ) from e

            self._operation_list = None
            now = datetime.datetime.now(datetime.UTC)
            self._wait_impl(deadline - now)
            return

        msg = (
            "An invalid operation.\n"
            f"operation: {operation}\n"
            f"index: {index}"
        )
        raise InvalidOperation(msg, self._browser.get_screenshot())
