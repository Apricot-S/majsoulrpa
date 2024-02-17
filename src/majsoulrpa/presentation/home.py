import datetime
import re
import time
from enum import IntEnum
from logging import getLogger
from typing import Literal

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .exceptions import (
    InconsistentMessageError,
    PresentationNotDetectedError,
    PresentationTimeoutError,
)
from .presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)

logger = getLogger(__name__)


class JoinRoomFailureReason(IntEnum):
    """Indicates the reason for failure to join a friendly match room.

    Attributes:
        NOT_FOUND: The room was not found.
        FULL: The room was full.
        ALREADY_STARTED: A match was already started.
    """

    NOT_FOUND = 1100
    FULL = 1101
    ALREADY_STARTED = 1109


class HomePresentation(PresentationBase):
    """Home presentation.

    The `HomePresentation` represents the main game screen, often
    referred to as the "lobby" screen, which is displayed after
    successfully completing the login/authentication process. Users can
    perform the following operations with an instance of
    `HomePresentation`:

    * Create a room for friendly matches.
    * Join a room for friendly matches by entering a room ID.
    """

    @staticmethod
    def _match_markers(screenshot: bytes, zoom_ratio: float) -> bool:
        for i in range(1, 4):
            template = Template.open_file(
                f"template/home/marker{i}",
                zoom_ratio,
            )
            if not template.match(screenshot):
                return False
        return True

    @staticmethod
    def _receive_daily_bonus(
        browser: BrowserBase,
        deadline: datetime.datetime,
    ) -> None:
        """Receive the daily bonus by clicking on the jade
        that appears at the end of the fortune charm animation.

        """
        jade = Template.open_file("template/home/jade", browser.zoom_ratio)
        jade.wait_until_then_click(browser, deadline)
        time.sleep(0.4)

    @staticmethod
    def _close_notifications(
        browser: BrowserBase,
        deadline: datetime.datetime,
    ) -> None:
        """Close home screen notifications if they are visible.

        Note:
            Does not support special events such as
            collaboration events.

        """
        notification_close = Template.open_file(
            "template/home/notification_close",
            browser.zoom_ratio,
        )
        event_close = Template.open_file(
            "template/home/event_close",
            browser.zoom_ratio,
        )
        rewards_sign_in = Template.open_file(
            "template/home/accumulated_sign_in_rewards_sign_in",
            browser.zoom_ratio,
        )

        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise PresentationTimeoutError(msg, browser.get_screenshot())

            ss = browser.get_screenshot()

            x, y, score = notification_close.best_template_match(ss)
            if score >= notification_close.threshold:
                browser.click_region(
                    x,
                    y,
                    notification_close.img_width,
                    notification_close.img_height,
                )
                time.sleep(1.0)
                continue

            x, y, score = event_close.best_template_match(ss)
            if score >= event_close.threshold:
                browser.click_region(
                    x,
                    y,
                    event_close.img_width,
                    event_close.img_height,
                )
                time.sleep(1.0)
                continue

            x, y, score = rewards_sign_in.best_template_match(ss)
            if score >= rewards_sign_in.threshold:
                browser.click_region(
                    x,
                    y,
                    rewards_sign_in.img_width,
                    rewards_sign_in.img_height,
                )
                time.sleep(1.9)

                rewards_confirm = Template.open_file(
                    "template/home/accumulated_sign_in_rewards_confirm",
                    browser.zoom_ratio,
                )
                while True:
                    if datetime.datetime.now(datetime.UTC) > deadline:
                        msg = "Timeout."
                        raise PresentationTimeoutError(
                            msg,
                            browser.get_screenshot(),
                        )
                    ss = browser.get_screenshot()
                    x, y, score = rewards_confirm.best_template_match(ss)
                    if score >= rewards_confirm.threshold:
                        browser.click_region(
                            x,
                            y,
                            rewards_confirm.img_width,
                            rewards_confirm.img_height,
                        )
                        break

                continue

            break

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType) -> None:
        template = Template.open_file(
            "template/home/marker0",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def __init__(  # noqa: C901
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> None:
        """Creates an instance of `HomePresentation`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            browser: The browser instance currently displaying the home
                screen.
            message_queue_client: A message queue client currently
                connected to the queue where mitmproxy is pushing
                messages.
            creator: A presentation creator responsible for
                instantiating presentations.
            timeout: The maximum duration, in seconds, to wait for the
                exchange of messages related to authentication and login
                to complete.

        Raises:
            PresentationNotDetectedError: If the home screen is not
                detected.
            PresentationTimeoutError: If the following conditions do not
                complete within the specified timeout period: (1) The
                exchange of messages related to authentication and
                login. (2) The display of the home screen, which
                includes finishing all operations such as acquiring
                jades through a valid Fortune Charm, closing
                announcement dialog boxes, and ultimately reaching a
                state where the "Ranked Match," "Tournament Match," and
                "Friendly Match" buttons are clickable.
            InconsistentMessageError: If an unexpected message is found
                in the message queue.
        """
        super().__init__(browser, message_queue_client, creator)

        deadline = timeout_to_deadline(timeout)

        template = Template.open_file(
            "template/home/marker0",
            browser.zoom_ratio,
        )
        ss = browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `HomePresentation`."
            raise PresentationNotDetectedError(msg, ss)

        has_month_ticket = False
        num_login_beats = 0
        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout."
                raise PresentationTimeoutError(msg, browser.get_screenshot())
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.Lobby.heatbeat"
                    | ".lq.NotifyReviveCoinUpdate"
                    | ".lq.NotifyGiftSendRefresh"
                    | ".lq.NotifyDailyTaskUpdate"
                    | ".lq.NotifyAccountChallengeTaskUpdate"
                    | ".lq.NotifyActivityChange"
                    | ".lq.NotifyAccountUpdate"  # TODO: Analyzing content
                    | ".lq.NotifyShopUpdate"  # TODO: Analyzing content
                    | ".lq.Lobby.oauth2Auth"
                    | ".lq.Lobby.oauth2Check"
                    | ".lq.NotifyNewMail"
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
                    | ".lq.Lobby.fetchReviveCoinInfo"
                    | ".lq.Lobby.fetchTitleList"
                    | ".lq.Lobby.fetchBagInfo"
                    | ".lq.Lobby.fetchShopInfo"
                    | ".lq.Lobby.fetchShopInterval"
                    | ".lq.Lobby.fetchActivityList"
                    | ".lq.Lobby.fetchActivityInterval"
                    | ".lq.Lobby.fetchActivityBuff"
                    | ".lq.Lobby.fetchVipReward"
                    | ".lq.Lobby.fetchMonthTicketInfo"
                    | ".lq.Lobby.fetchAchievement"
                    | ".lq.Lobby.fetchSelfGamePointRank"
                    | ".lq.Lobby.fetchCommentSetting"
                    | ".lq.Lobby.fetchAccountSettings"
                    | ".lq.Lobby.fetchModNicknameTime"
                    | ".lq.Lobby.fetchMisc"
                    | ".lq.Lobby.fetchAnnouncement"
                    | ".lq.Lobby.fetchRollingNotice"
                    | ".lq.Lobby.loginSuccess"
                    | ".lq.Lobby.fetchCharacterInfo"
                    | ".lq.Lobby.fetchAllCommonViews"
                    | ".lq.Lobby.fetchCollectedGameRecordList"
                    | ".lq.Lobby.modifyRoom"
                    | ".lq.NotifyRoomPlayerReady"
                    | ".lq.Lobby.readyPlay"
                    | ".lq.Lobby.fetchInfo"  # TODO: Analyzing content
                    | ".lq.Lobby.fetchActivityFlipInfo"
                    | ".lq.Lobby.fetchCustomizedContestList"
                    | ".lq.Lobby.fetchCustomizedContestExtendInfo"
                    | ".lq.Lobby.fetchCustomizedContestOnlineInfo"
                    | ".lq.Lobby.startCustomizedContest"
                    | ".lq.Lobby.stopCustomizedContest"
                ):
                    logger.info(message)
                    continue
                case ".lq.Lobby.payMonthTicket":
                    logger.info(message)
                    has_month_ticket = True
                    continue
                case (
                    ".lq.Lobby.fetchDailyTask"
                    | ".lq.Lobby.leaveRoom"
                    | ".lq.Lobby.leaveCustomizedContest"
                    | ".lq.Lobby.leaveCustomizedContestChatRoom"
                    | ".lq.Lobby.fetchAccountActivityData"
                ):
                    logger.info(message)

                    break_ = False
                    while True:
                        next_message = (
                            self._message_queue_client.dequeue_message(5)
                        )
                        if next_message is None:
                            # If there are no more messages,
                            # the transition to the home screen
                            # has been completed.
                            break_ = True
                            break
                        _, next_name, _, _, _ = next_message
                        if next_name == ".lq.Lobby.heatbeat":
                            # Discard subsequent
                            # `.lq.Lobby.heatbeat` messages.
                            logger.info(next_message)
                            continue
                        # Backfill the prefetched message and
                        # proceed to the next.
                        self._message_queue_client.put_back(next_message)
                        break
                    if break_:
                        break
                    continue
                case ".lq.Lobby.loginBeat":
                    logger.info(message)
                    num_login_beats += 1
                    if num_login_beats == 2:  # noqa: PLR2004
                        break
                    continue
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        browser.get_screenshot(),
                    )

        while True:
            message = self._message_queue_client.dequeue_message(0.1)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.Lobby.heatbeat"
                    | ".lq.Lobby.updateClientValue"
                    | ".lq.NotifyAccountUpdate"
                    | ".lq.NotifyAnnouncementUpdate"
                    | ".lq.Lobby.readAnnouncement"
                    | ".lq.Lobby.doActivitySignIn"
                    | ".lq.Lobby.fetchDailyTask"  # TODO: Analyzing content
                ):
                    logger.info(message)
                    continue
                case ".lq.Lobby.payMonthTicket":
                    logger.info(message)
                    has_month_ticket = True
                    continue
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        browser.get_screenshot(),
                    )

        # Wait for markers to display on the home screen.
        time.sleep(0.5)

        if not HomePresentation._match_markers(
            browser.get_screenshot(),
            browser.zoom_ratio,
        ):
            if has_month_ticket:
                HomePresentation._receive_daily_bonus(browser, deadline)
            HomePresentation._close_notifications(browser, deadline)

            while True:
                if datetime.datetime.now(datetime.UTC) > deadline:
                    msg = "Timeout."
                    raise PresentationTimeoutError(
                        msg,
                        browser.get_screenshot(),
                    )
                if HomePresentation._match_markers(
                    browser.get_screenshot(),
                    browser.zoom_ratio,
                ):
                    break

    def _discard_messages_across_dates(self) -> None:
        while True:
            message = self._message_queue_client.dequeue_message(0.1)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.NotifyReviveCoinUpdate"
                    | ".lq.NotifyGiftSendRefresh"
                    | ".lq.NotifyDailyTaskUpdate"
                    | ".lq.NotifyActivityPeriodTaskUpdate"
                    | ".lq.NotifyShopUpdate"
                    | ".lq.NotifyAccountChallengeTaskUpdate"
                    | ".lq.NotifyAccountUpdate"
                    | ".lq.Lobby.fetchShopInterval"
                    | ".lq.Lobby.fetchActivityInterval"
                    | ".lq.Lobby.heatbeat"
                ):
                    logger.info(message)
                    continue
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    )

    def enter_tournament(
        self,
        tournament_id: str,
        timeout: TimeoutType = 60.0,
    ) -> bool:
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        if re.fullmatch(r"\d{6}", tournament_id) is None:
            msg = "Tournament ID must be a 6-digit number."
            raise ValueError(msg)

        self._discard_messages_across_dates()

        # Click "Tournament Match".
        template = Template.open_file(
            "template/home/marker2",
            self._browser.zoom_ratio,
        )
        template.click(self._browser)

        # Wait until "Tournament Lobby" is displayed and then click.
        template = Template.open_file(
            "template/home/tournament_lobby",
            self._browser.zoom_ratio,
        )
        template.wait_until_then_click(self._browser, deadline)

        template = Template.open_file(
            "template/home/tournament_lobby/marker",
            self._browser.zoom_ratio,
        )
        template.wait_until(self._browser, deadline)

        while True:
            message = self._message_queue_client.dequeue_message(1)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.Lobby.heatbeat"
                    | ".lq.Lobby.fetchCustomizedContestList"
                    | ".lq.Lobby.fetchCustomizedContestExtendInfo"
                ):
                    logger.info(message)
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    )

        # Wait until "Enter Tournament ID" is displayed and then click.
        template = Template.open_file(
            "template/home/tournament_lobby/enter_tournament_id",
            self._browser.zoom_ratio,
        )
        template.wait_until_then_click(self._browser, deadline)

        # Wait until "Confirm" is displayed.
        template = Template.open_file(
            "template/home/tournament_lobby/confirm",
            self._browser.zoom_ratio,
        )
        template.wait_until(self._browser, deadline)

        # Click the text box to focus it.
        self._browser.click_region(
            int(660 * self._browser.zoom_ratio),
            int(340 * self._browser.zoom_ratio),
            int(410 * self._browser.zoom_ratio),
            int(40 * self._browser.zoom_ratio),
        )
        time.sleep(0.1)

        # Enter an room id in the text box.
        self._browser.write(tournament_id)

        # Click "Confirm"
        template.click(self._browser)

        try:
            template = Template.open_file(
                "template/home/tournament_lobby/error_close",
                self._browser.zoom_ratio,
            )
            template.wait_for_then_click(self._browser, 1.5)
        except PresentationTimeoutError:
            pass
        else:
            time.sleep(0.5)

            while True:
                message = self._message_queue_client.dequeue_message(1)
                if message is None:
                    break
                _, name, _, _, _ = message

                match name:
                    case (
                        ".lq.Lobby.heatbeat"
                        | ".lq.Lobby.fetchCustomizedContestByContestId"
                    ):
                        logger.info(message)
                    case _:
                        raise InconsistentMessageError(
                            str(message),
                            self._browser.get_screenshot(),
                        )

            # Click on the icon to leave the tournament lobby.
            template = Template.open_file(
                "template/home/tournament_lobby/leave",
                self._browser.zoom_ratio,
            )
            template.wait_until_then_click(self._browser, deadline)
            time.sleep(1.5)

            return False

        # Wait until tournament lobby screen is displayed.
        now = datetime.datetime.now(datetime.UTC)
        self._creator.wait(
            self._browser,
            deadline - now,
            Presentation.TOURNAMENT,
        )

        now = datetime.datetime.now(datetime.UTC)
        new_presentation = self._creator.create_new_presentation(
            Presentation.HOME,
            Presentation.TOURNAMENT,
            self._browser,
            self._message_queue_client,
        )
        self._set_new_presentation(new_presentation)

        return True

    def create_room(
        self,
        mode: Literal["4-Player", "3-Player"] = "4-Player",
        length: Literal[
            "1 Game",
            "East Only",
            "Two-Wind Match",
            "Vs AI",
        ] = "Two-Wind Match",
        timeout: TimeoutType = 60.0,
    ) -> None:
        """Creates a room for friendly matches.

        Initiates a transition to the `RoomHostPresentation` by creating
        a room for friendly matches, and waits for the room screen to
        appear.

        Args:
            mode: The mode of the room. Defaults to "4-Player".
            length: The length of matches in the room. Defaults to
                "Two-Wind Match".
            timeout: The maximum duration, in seconds, to wait for the
                room screen to appear. Defaults to `60.0`.

        Raises:
            PresentationTimeoutError: If the room screen does not
                appear within the specified timeout period.
            ValueError: If an unsupported mode or length is selected.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)
        self._discard_messages_across_dates()

        # Click "Friendly Match".
        template = Template.open_file(
            "template/home/marker3",
            self._browser.zoom_ratio,
        )
        template.click(self._browser)

        # Wait until "Create room" is displayed and then click.
        template = Template.open_file(
            "template/home/create_room",
            self._browser.zoom_ratio,
        )
        template.wait_until_then_click(self._browser, deadline)

        # Wait until "Create" is displayed.
        template = Template.open_file(
            "template/home/room_creation/create",
            self._browser.zoom_ratio,
        )
        template.wait_until(self._browser, deadline)

        def select_option(selected: str) -> None:
            template = Template.open_file(selected, self._browser.zoom_ratio)
            while True:
                if datetime.datetime.now(datetime.UTC) > deadline:
                    msg = "Timeout."
                    raise PresentationTimeoutError(
                        msg,
                        self._browser.get_screenshot(),
                    )
                if template.match(self._browser.get_screenshot()):
                    break
                template.click(self._browser)
                time.sleep(0.5)

        # Select Mode
        match mode:
            case "4-Player":
                select_option("template/home/room_creation/4-player")
            case "3-Player":
                select_option("template/home/room_creation/3-player")
            case _ as unsupported_mode:
                msg = f"Unsupported mode selected: {unsupported_mode}"
                raise ValueError(msg)

        # Select Length
        match length:
            case "1 Game":
                select_option("template/home/room_creation/1_game")
            case "East Only":
                select_option("template/home/room_creation/east_only")
            case "Two-Wind Match":
                select_option("template/home/room_creation/two-wind_match")
            case "Vs AI":
                select_option("template/home/room_creation/vs_ai")
            case _ as unsupported_length:
                msg = f"Unsupported length selected: {unsupported_length}"
                raise ValueError(msg)

        # Click "Create"
        template.click(self._browser)

        # Wait until room screen is displayed.
        now = datetime.datetime.now(datetime.UTC)
        self._creator.wait(
            self._browser,
            deadline - now,
            Presentation.ROOM_HOST,
        )

        now = datetime.datetime.now(datetime.UTC)
        new_presentation = self._creator.create_new_presentation(
            Presentation.HOME,
            Presentation.ROOM_HOST,
            self._browser,
            self._message_queue_client,
            timeout=(deadline - now),
        )
        self._set_new_presentation(new_presentation)

    def join_room(  # noqa: C901
        self,
        room_id: str,
        timeout: TimeoutType = 60.0,
    ) -> JoinRoomFailureReason | None:
        """Joins a room for friendly matches by entering a room ID.

        Attempts to initiate a transition to the `RoomGuestPresentation`
        by joining a room with the specified room ID, and waits for the
        room screen to appear.

        Args:
            room_id: The room ID to join.
            timeout: The maximum duration, in seconds, to wait for the
                room screen to appear. Defaults to `60.0`.

        Returns:
            `None` if successfully joined the room;
                `JoinRoomFailureReason` if the room ID is invalid or the
                transition fails for some reason.

        Raises:
            ValueError: If the room ID is not a 5-digit number.
        """
        if re.fullmatch(r"\d{5}", room_id) is None:
            msg = "Room ID must be a 5-digit number."
            raise ValueError(msg)

        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)
        self._discard_messages_across_dates()

        # Click "Friendly Match".
        template = Template.open_file(
            "template/home/marker3",
            self._browser.zoom_ratio,
        )
        template.click(self._browser)

        # Wait until "Join room" is displayed and then click.
        template = Template.open_file(
            "template/home/join_room",
            self._browser.zoom_ratio,
        )
        template.wait_until_then_click(self._browser, deadline)

        # Wait until "Confirm" is displayed.
        template = Template.open_file(
            "template/home/room_join/confirm",
            self._browser.zoom_ratio,
        )
        template.wait_until(self._browser, deadline)

        # Click the text box to focus it.
        self._browser.click_region(
            int(660 * self._browser.zoom_ratio),
            int(340 * self._browser.zoom_ratio),
            int(410 * self._browser.zoom_ratio),
            int(40 * self._browser.zoom_ratio),
        )
        time.sleep(0.1)

        # Enter an room id in the text box.
        self._browser.write(room_id)

        # Click "Confirm"
        template.click(self._browser)

        try:
            template = Template.open_file(
                "template/home/room_join/error_close",
                self._browser.zoom_ratio,
            )
            template.wait_for(self._browser, 1.5)
        except PresentationTimeoutError:
            pass
        else:
            # For check the error code and reason for the error.
            ss = self._browser.get_screenshot()

            template.click(self._browser)
            time.sleep(0.5)

            # Click "Back".
            self._browser.click_region(
                int(1175 * self._browser.zoom_ratio),
                int(250 * self._browser.zoom_ratio),
                int(100 * self._browser.zoom_ratio),
                int(34 * self._browser.zoom_ratio),
            )
            time.sleep(1.0)

            reason = None
            while True:
                if datetime.datetime.now(datetime.UTC) > deadline:
                    msg = "Timeout."
                    raise PresentationTimeoutError(msg, ss)

                message = self._message_queue_client.dequeue_message(1)
                if message is None:
                    if reason is not None:
                        return reason
                    msg = "`.lq.Lobby.joinRoom` was not exchanged."
                    raise InconsistentMessageError(msg, ss)
                _, name, _, response, _ = message

                match name:
                    case ".lq.Lobby.joinRoom":
                        if response is None:
                            # If there was no response that was supposed
                            # to be there.
                            raise InconsistentMessageError(str(message), ss)

                        try:
                            error_code: int = response["error"]["code"]
                        except KeyError as k:
                            # If there was no error code that was
                            # supposed to be there.
                            raise InconsistentMessageError(
                                str(message),
                                ss,
                            ) from k

                        try:
                            reason = JoinRoomFailureReason(error_code)
                        except ValueError as v:
                            # In case of unknown error code.
                            raise InconsistentMessageError(
                                str(message),
                                ss,
                            ) from v

                        logger.info(message)
                    case ".lq.Lobby.heatbeat":
                        logger.info(message)
                    case _:
                        raise InconsistentMessageError(str(message), ss)

        # Wait until room screen is displayed.
        now = datetime.datetime.now(datetime.UTC)
        self._creator.wait(
            self._browser,
            deadline - now,
            Presentation.ROOM_GUEST,
        )

        now = datetime.datetime.now(datetime.UTC)
        new_presentation = self._creator.create_new_presentation(
            Presentation.HOME,
            Presentation.ROOM_GUEST,
            self._browser,
            self._message_queue_client,
            timeout=(deadline - now),
        )
        self._set_new_presentation(new_presentation)

        return None
