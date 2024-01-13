import datetime
import re
import time
from logging import getLogger
from typing import Literal

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .presentation_base import (
    InconsistentMessage,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetected,
    Timeout,
)

logger = getLogger(__name__)


class HomePresentation(PresentationBase):
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
    def _close_notifications(
        browser: BrowserBase,
        deadline: datetime.datetime,
    ) -> None:
        """Close home screen notifications if they are visible."""

        # Wait for the fortune charm's effect to end.
        try:
            jade = Template.open_file("template/home/jade", browser.zoom_ratio)
            jade.wait_for_then_click(browser, 4.0)
        except Timeout:
            pass
        else:
            time.sleep(0.4)

        notification_close = Template.open_file(
            "template/home/notification_close",
            browser.zoom_ratio,
        )
        event_close = Template.open_file(
            "template/home/event_close",
            browser.zoom_ratio,
        )

        # TODO(Apricot S): Add processing for  # noqa: TD003
        # "Sign-in" and "Confirm" for limited time login bonus
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, browser.get_screenshot())

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

            break

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType) -> None:
        template = Template.open_file(
            "template/home/marker0",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def __init__(  # noqa: PLR0912, PLR0915, C901
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> None:
        super().__init__(browser, message_queue_client, creator)

        deadline = timeout_to_deadline(timeout)

        template = Template.open_file(
            "template/home/marker0",
            browser.zoom_ratio,
        )
        ss = browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `HomePresentation`."
            raise PresentationNotDetected(msg, ss)

        # Wait for markers to display on the home screen.
        time.sleep(0.5)

        if not HomePresentation._match_markers(
            browser.get_screenshot(),
            browser.zoom_ratio,
        ):
            # Close any notifications displayed on the home screen.
            HomePresentation._close_notifications(browser, deadline)

            while True:
                if datetime.datetime.now(datetime.UTC) > deadline:
                    msg = "Timeout."
                    raise Timeout(msg, browser.get_screenshot())
                if HomePresentation._match_markers(
                    browser.get_screenshot(),
                    browser.zoom_ratio,
                ):
                    break

        num_login_beats = 0
        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(
                deadline - now,
            )
            if message is None:
                msg = "Timeout."
                raise Timeout(msg, browser.get_screenshot())
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
                    | ".lq.Lobby.payMonthTicket"
                    | ".lq.Lobby.fetchInfo"  # TODO: Analyzing content
                ):
                    logger.info(message)
                    continue
                case (
                    ".lq.Lobby.fetchDailyTask"
                    | ".lq.Lobby.leaveRoom"
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

            raise InconsistentMessage(str(message), browser.get_screenshot())

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
                    | ".lq.Lobby.payMonthTicket"
                ):
                    logger.info(message)
                    continue
                case ".lq.Lobby.fetchDailyTask":  # TODO: Analyzing content
                    logger.info(message)

                    # If there are no more messages,
                    # the transition to the home screen
                    # has been completed.
                    message = self._message_queue_client.dequeue_message(5)
                    if message is None:
                        return

                    # Backfill the prefetched message and
                    # proceed to the next.
                    self._message_queue_client.put_back(message)
                    continue

            raise InconsistentMessage(str(message), browser.get_screenshot())

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
                    raise InconsistentMessage(
                        str(message),
                        self._browser.get_screenshot(),
                    )

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
                    raise Timeout(msg, self._browser.get_screenshot())
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

    def join_room(
        self,
        room_id: str,
        timeout: TimeoutType = 60.0,
    ) -> bool:
        if re.match(r"(\d{5})", room_id) is None:
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

        template = Template.open_file(
            "template/home/room_join/error_close",
            self._browser.zoom_ratio,
        )
        try:
            template.wait_for_then_click(self._browser, 1.5)
        except Timeout:
            pass
        else:
            time.sleep(0.5)
            # Click "Back".
            self._browser.click_region(
                int(1175 * self._browser.zoom_ratio),
                int(250 * self._browser.zoom_ratio),
                int(100 * self._browser.zoom_ratio),
                int(34 * self._browser.zoom_ratio),
            )
            time.sleep(1.0)

            while True:
                message = self._message_queue_client.dequeue_message(0.1)
                if message is None:
                    break
                logger.info(message)

            return False

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

        return True
