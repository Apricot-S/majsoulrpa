import datetime
import time
from collections.abc import Iterable, Mapping
from logging import getLogger
from typing import Self

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline
from majsoulrpa.presentation.exceptions import (
    InconsistentMessageError,
    InvalidOperationError,
    PresentationNotDetectedError,
    PresentationTimeoutError,
)
from majsoulrpa.presentation.presentation_base import (
    Presentation,
    PresentationCreatorBase,
)

from .base import RoomPlayer, RoomPresentationBase

logger = getLogger(__name__)


class RoomHostPresentation(RoomPresentationBase):
    """Room host presentation.

    Represents the room screen as seen by the host. Users can perform
    the following operations with an instance of `RoomHostPresentation`:

    * Add AI players to the room.
    * Start a match.
    """

    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        room_id: int,
        max_num_players: int,
        players: Iterable[RoomPlayer],
        num_ais: int,
    ) -> None:
        """Creates an instance of `RoomHostPresentation`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            browser: The browser instance currently displaying the room
                screen.
            message_queue_client: A message queue client currently
                connected to the queue where mitmproxy is pushing
                messages.
            creator: A presentation creator responsible for
                instantiating presentations.
            room_id: The room ID.
            max_num_players: The maximum number of players allowed in
                the room.
            players: The players in the room.
            num_ais: The number of AI players in the room.
        """
        super().__init__(
            browser,
            message_queue_client,
            creator,
            room_id,
            max_num_players,
            players,
            num_ais,
        )

    @classmethod
    def _create(
        cls,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> Self:
        deadline = timeout_to_deadline(timeout)

        template = Template.open_file(
            "template/room/marker",
            browser.zoom_ratio,
        )
        ss = browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `room`."
            raise PresentationNotDetectedError(msg, ss)

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = message_queue_client.dequeue_message(deadline - now)
            if message is None:
                msg = "Timeout."
                raise PresentationTimeoutError(msg, ss)
            _, name, _, response, _ = message

            match name:
                case ".lq.Lobby.heatbeat" | ".lq.FastTest.checkNetworkDelay":
                    logger.info(message)
                    continue
                case ".lq.Lobby.createRoom" | ".lq.Lobby.fetchRoom":
                    logger.info(message)
                    break

            raise InconsistentMessageError(str(message), ss)

        if not isinstance(response, Mapping):
            msg = f"`{name}` response does not have a dict."
            raise InconsistentMessageError(msg)

        room: dict = response["room"]
        room_id: int = room["room_id"]
        owner_id: int = room["owner_id"]
        if owner_id != message_queue_client.account_id:
            raise InconsistentMessageError(str(message), ss)
        max_num_players: int = room["max_player_count"]
        ready_list: list[int] = room["ready_list"]
        players: list[RoomPlayer] = []
        for person in room["persons"]:
            account_id = person["account_id"]
            player = RoomPlayer(
                account_id,
                person["nickname"],
                is_host=(account_id == owner_id),
                is_ready=(account_id in ready_list),
            )
            players.append(player)
        num_ais = room["robot_count"]

        return cls(
            browser,
            message_queue_client,
            creator,
            room_id,
            max_num_players,
            players,
            num_ais,
        )

    @classmethod
    def _return_from_match(
        cls,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        prev_presentation: Self,
        timeout: TimeoutType,
    ) -> Self:
        deadline = timeout_to_deadline(timeout)

        now = datetime.datetime.now(datetime.UTC)
        cls._wait(browser, deadline - now)

        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise PresentationTimeoutError(msg, browser.get_screenshot())

            now = datetime.datetime.now(datetime.UTC)
            message = message_queue_client.dequeue_message(deadline - now)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case ".lq.Lobby.heatbeat":
                    logger.info(message)
                    continue
                case ".lq.Lobby.fetchAccountInfo":
                    # TODO(Apricot-S): Update account information
                    logger.info(message)
                    continue
                case ".lq.Lobby.fetchRoom":
                    # TODO(Apricot-S): Update of room information
                    logger.info(message)
                    continue

            raise InconsistentMessageError(name, browser.get_screenshot())

        return cls(
            browser,
            message_queue_client,
            creator,
            prev_presentation.room_id,
            prev_presentation.max_num_players,
            prev_presentation.players,
            prev_presentation.num_ais,
        )

    def add_ai(self, timeout: TimeoutType = 10.0) -> None:
        """Adds an AI player to the room.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                AI to be added. Defaults to `10.0`.

        Raises:
            InvalidOperationError: If the "Add AI" button is not
                clickable because the room is full.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        # Check if "Add AI" is clickable, and if so, click it.
        template = Template.open_file(
            "template/room/add_ai",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "Could not add AI."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        old_num_ais = self.num_ais

        # An effect occurs when you click "Add AI" and
        # the effect interferes with template matching
        # when you click "Add AI" consecutively,
        # so wait until the effect disappears.
        time.sleep(1.5)

        # Wait until WebSocket messages come in and
        # the number of AIs actually increases.
        while self.num_ais <= old_num_ais:
            now = datetime.datetime.now(datetime.UTC)
            self._update(deadline - now)

    def start(self, timeout: TimeoutType = 60.0) -> None:
        """Starts a match.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                match to start. Defaults to `60.0`.

        Raises:
            PresentationTimeoutError: If the match does not start
                within the specified timeout period.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        template = Template.open_file(
            "template/room/start",
            self._browser.zoom_ratio,
        )
        template.wait_until_then_click(self._browser, deadline)

        now = datetime.datetime.now(datetime.UTC)
        self._creator.wait(self._browser, deadline - now, Presentation.MATCH)

        now = datetime.datetime.now(datetime.UTC)
        new_presentation = self._creator.create_new_presentation(
            Presentation.ROOM_HOST,
            Presentation.MATCH,
            self._browser,
            self._message_queue_client,
            timeout=(deadline - now),
        )
        self._set_new_presentation(new_presentation)
