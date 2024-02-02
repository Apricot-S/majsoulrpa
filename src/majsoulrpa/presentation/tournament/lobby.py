import datetime
import re
import time
from logging import getLogger

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline
from majsoulrpa.presentation.presentation_base import (
    InconsistentMessageError,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetectedError,
    PresentationTimeoutError,
)

logger = getLogger(__name__)


class TournamentLobbyPresentation(PresentationBase):
    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
        super().__init__(browser, message_queue_client, creator)

        template = Template.open_file(
            "template/tournament/lobby/marker",
            browser.zoom_ratio,
        )
        ss = browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `TournamentLobbyPresentation`."
            raise PresentationNotDetectedError(msg, ss)

        while True:
            message = self._message_queue_client.dequeue_message(0.1)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case (
                    ".lq.Lobby.fetchCustomizedContestList"
                    | ".lq.Lobby.fetchCustomizedContestExtendInfo"
                ):
                    logger.info(message)
                    continue
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        browser.get_screenshot(),
                    )

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 10.0) -> None:
        template = Template.open_file(
            "template/tournament/lobby/marker",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def enter_room(
        self,
        tournament_id: str,
        timeout: TimeoutType = 60.0,
    ) -> bool:
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        if re.fullmatch(r"\d{6}", tournament_id) is None:
            msg = "Tournament ID must be a 6-digit number."
            raise ValueError(msg)

        # Wait until "Enter Tournament ID" is displayed and then click.
        template = Template.open_file(
            "template/tournament/lobby/enter_tournament_id",
            self._browser.zoom_ratio,
        )
        template.wait_until_then_click(self._browser, deadline)

        # Wait until "Confirm" is displayed.
        template = Template.open_file(
            "template/tournament/lobby/confirm",
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

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = self._message_queue_client.dequeue_message(0.1)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case ".lq.Lobby.fetchCustomizedContestByContestId":
                    logger.info(message)
                    continue
                case _:
                    raise InconsistentMessageError(
                        str(message),
                        self._browser.get_screenshot(),
                    )

        try:
            template = Template.open_file(
                "template/tournament/lobby/error_close",
                self._browser.zoom_ratio,
            )
            template.wait_for_then_click(self._browser, 1.5)
        except PresentationTimeoutError:
            pass
        else:
            time.sleep(0.5)

            while True:
                message = self._message_queue_client.dequeue_message(0.1)
                if message is None:
                    break
                logger.info(message)

            return False

        return True  # TODO Transition to tournament room

        # Wait until room screen is displayed.
        now = datetime.datetime.now(datetime.UTC)
        self._creator.wait(
            self._browser,
            deadline - now,
            Presentation.TOURNAMENT_ROOM,
        )

        now = datetime.datetime.now(datetime.UTC)
        new_presentation = self._creator.create_new_presentation(
            Presentation.TOURNAMENT_LOBBY,
            Presentation.TOURNAMENT_ROOM,
            self._browser,
            self._message_queue_client,
            timeout=(deadline - now),
        )
        self._set_new_presentation(new_presentation)

        return True
