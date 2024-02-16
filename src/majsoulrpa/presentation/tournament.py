import datetime
import time
from logging import getLogger

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .presentation_base import (
    InconsistentMessageError,
    InvalidOperationError,
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

    def _validate_participation_availability(self) -> None:
        ss = self._browser.get_screenshot()

        template = Template.open_file(
            "template/tournament/match_hasnt_started",
            self._browser.zoom_ratio,
        )
        if template.match(ss):
            msg = "The tournament match hasn't started."
            raise InvalidOperationError(msg, ss)

        template = Template.open_file(
            "template/tournament/match_has_ended",
            self._browser.zoom_ratio,
        )
        if template.match(ss):
            msg = "The tournament match has ended."
            raise InvalidOperationError(msg, ss)

        template0 = Template.open_file(
            "template/tournament/prepare_for_match",
            self._browser.zoom_ratio,
        )
        template1 = Template.open_file(
            "template/tournament/waiting_to_start",
            self._browser.zoom_ratio,
        )
        if Template.match_one_of(ss, [template0, template1]) == -1:
            msg = (
                "Unexpected state: "
                "The tournament room may have been closed. "
                "Please cooperate by providing a screenshot of the error. "
                "Thank you for your cooperation."
            )
            error = UnexpectedStateError(msg, ss)
            error.save_screenshot()
            raise error

    def prepare(
        self,
        timeout: TimeoutType = 60.0,
    ) -> None:
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        self._validate_participation_availability()

        # Click on "Prepare for match".
        template = Template.open_file(
            "template/tournament/prepare_for_match",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "There was no tournament being held."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Clicking "Prepare for match" will generate an effect,
        # which will interfere with template matching,
        # so wait until the effect disappears.
        time.sleep(1.5)

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
                # Clicking "Waiting to start..." will generate an
                # effect, which will interfere with template matching,
                # so wait until the effect disappears.
                time.sleep(1.5)
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

        ss = self._browser.get_screenshot()

        template0 = Template.open_file(
            "template/tournament/match_hasnt_started",
            self._browser.zoom_ratio,
        )
        template1 = Template.open_file(
            "template/tournament/match_has_ended",
            self._browser.zoom_ratio,
        )
        template2 = Template.open_file(
            "template/tournament/prepare_for_match",
            self._browser.zoom_ratio,
        )
        template3 = Template.open_file(
            "template/tournament/waiting_to_start",
            self._browser.zoom_ratio,
        )
        templates = [template0, template1, template2, template3]

        if Template.match_one_of(ss, templates) == -1:
            msg = (
                "Unexpected state: "
                "The tournament room may have been closed. "
                "Please cooperate by providing a screenshot of the error. "
                "Thank you for your cooperation."
            )
            error = UnexpectedStateError(msg, ss)
            error.save_screenshot()
            raise error

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

        new_presentation = self._creator.create_new_presentation(
            Presentation.TOURNAMENT,
            Presentation.HOME,
            self._browser,
            self._message_queue_client,
            timeout=timeout,
        )
        self._set_new_presentation(new_presentation)
