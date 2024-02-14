import datetime
import time
from logging import getLogger

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .presentation_base import (
    InconsistentMessageError,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetectedError,
    PresentationTimeoutError,
    UnexpectedStateError,
)

logger = getLogger(__name__)

__all__ = [
    "TournamentPresentation",
]


class TournamentPresentation(PresentationBase):
    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
        super().__init__(browser, message_queue_client, creator)

        template = Template.open_file(
            "template/tournament/marker",
            browser.zoom_ratio,
        )
        ss = browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `TournamentPresentation`."
            raise PresentationNotDetectedError(msg, ss)

        while True:
            message = self._message_queue_client.dequeue_message(1)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.Lobby.heatbeat"
                    | ".lq.Lobby.fetchCustomizedContestByContestId"
                    | ".lq.Lobby.enterCustomizedContest"
                    | ".lq.Lobby.joinCustomizedContestChatRoom"
                    | ".lq.Lobby.fetchCustomizedContestOnlineInfo"
                    | ".lq.NotifyCustomContestSystemMsg"
                ):
                    logger.info(message)
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        browser.get_screenshot(),
                    )

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 10.0) -> None:
        template = Template.open_file(
            "template/tournament/marker",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def prepare(
        self,
        timeout: TimeoutType = 60.0,
    ) -> None:
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        # Click on "Prepare for match".
        template = Template.open_file(
            "template/tournament/prepare_for_match",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "There was no tournament being held."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        try:
            now = datetime.datetime.now(datetime.UTC)
            self._creator.wait(
                self._browser,
                deadline - now,
                Presentation.MATCH,
            )
        except PresentationTimeoutError:
            cancel_template = Template.open_file(
                "template/tournament/waiting_to_start",
                self._browser.zoom_ratio,
            )
            if cancel_template.click_if_match(self._browser):
                return
            raise
        else:
            now = datetime.datetime.now(datetime.UTC)
            new_presentation = self._creator.create_new_presentation(
                Presentation.TOURNAMENT,
                Presentation.MATCH,
                self._browser,
                self._message_queue_client,
                timeout=(deadline - now),
            )
            self._set_new_presentation(new_presentation)

    def leave(self, timeout: TimeoutType = 10.0) -> None:
        self._assert_not_stale()

        # Click on the icon to leave the tournament room.
        template = Template.open_file(
            "template/tournament/leave",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "Could not leave the tournament room."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Wait until the tournament lobby is displayed.
        time.sleep(1.5)

        # Click on the icon to leave the tournament lobby.
        template = Template.open_file(
            "template/home/tournament_lobby/leave",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "Could not leave the tournament lobby."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Wait until the home screen is displayed.
        self._creator.wait(self._browser, timeout, Presentation.HOME)

        # TODO: __init__ fails because message is not exchanged
        new_presentation = self._creator.create_new_presentation(
            Presentation.TOURNAMENT,
            Presentation.HOME,
            self._browser,
            self._message_queue_client,
            timeout=timeout,
        )
        self._set_new_presentation(new_presentation)
