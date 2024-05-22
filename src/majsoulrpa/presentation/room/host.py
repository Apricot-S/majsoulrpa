import datetime
import time
from collections.abc import Iterable, Mapping
from logging import getLogger
from typing import Self

from majsoulrpa import RPA
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline
from majsoulrpa.presentation.exceptions import (
    InconsistentMessageError,
    InvalidOperationError,
    PresentationNotDetectedError,
    PresentationTimeoutError,
    UnexpectedStateError,
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
        rpa: RPA,
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
            rpa: A RPA client for Mahjong Soul.
            creator: A presentation creator responsible for
                instantiating presentations.
            room_id: The room ID.
            max_num_players: The maximum number of players allowed in
                the room.
            players: The players in the room.
            num_ais: The number of AI players in the room.
        """
        super().__init__(
            rpa,
            creator,
            room_id,
            max_num_players,
            players,
            num_ais,
        )

    @classmethod
    def _create(
        cls,
        rpa: RPA,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> Self:
        deadline = timeout_to_deadline(timeout)

        browser = rpa._browser  # noqa: SLF001
        if browser is None:
            msg = "Browser is not running."
            raise RuntimeError(msg)

        message_queue_client = rpa._message_queue_client  # noqa: SLF001
        if message_queue_client is None:
            msg = "Message queue client is not running."
            raise RuntimeError(msg)

        templates = (
            Template.open_file(
                "template/room/start",
                browser.zoom_ratio,
            ),
            Template.open_file(
                "template/room/start_disabled",
                browser.zoom_ratio,
            ),
        )
        ss = browser.get_screenshot()
        if Template.match_one_of(ss, templates) == -1:
            msg = "Could not detect `RoomHostPresentation`."
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

        return cls(rpa, creator, room_id, max_num_players, players, num_ais)

    def add_ai(self, timeout: TimeoutType = 10.0) -> None:
        """Adds an AI player to the room.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                AI to be added. Defaults to `10.0`.

        Raises:
            InvalidOperationError: If the room is full.
            UnexpectedStateError: If the "Add AI" button is not
                clickable due to an unexpected state.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        self._update_until_latest(1)

        old_num_ais = self.num_ais
        if (old_num_ais + len(self.players)) >= self.max_num_players:
            msg = "Could not add AI because the room was full."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        # Check if "Add AI" is clickable, and if so, click it.
        # Note: Even if the room is full and the button is dark,
        # it still matches the template image.
        template = Template.open_file(
            "template/room/add_ai",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "Could not add AI because the button could not be clicked."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Clicking "Add AI" will generate an effect that will interfere
        # with template matching, so wait until the effect disappears.
        time.sleep(1.5)

        # Wait until WebSocket messages come in and the number of AIs
        # actually increases or the room is full.
        num_ais = old_num_ais
        while (
            num_ais <= old_num_ais
            and (num_ais + len(self.players)) < self.max_num_players
        ):
            now = datetime.datetime.now(datetime.UTC)
            self._update(deadline - now)
            num_ais = self.num_ais

        # If a guest enters the room just before clicking the "Add AI"
        # button and the room becomes full, resulting in the AI not
        # being able to be added.
        if num_ais <= old_num_ais:
            msg = "Could not add AI because the room was full."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

    def start(self, timeout: TimeoutType = 60.0) -> None:
        """Starts a match.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                match to start. Defaults to `60.0`.

        Raises:
            InvalidOperationError: If the match does not start because
                the "Start" button could not be clicked.
            PresentationTimeoutError: If the match does not start
                within the specified timeout period.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        template = Template.open_file(
            "template/room/start",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = (
                "The match could not start "
                "because the button could not be clicked."
            )
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        now = datetime.datetime.now(datetime.UTC)
        self._creator.wait(self._browser, deadline - now, Presentation.MATCH)

        now = datetime.datetime.now(datetime.UTC)
        new_presentation = self._creator.create_new_presentation(
            Presentation.ROOM_HOST,
            Presentation.MATCH,
            self._rpa,
            timeout=(deadline - now),
        )
        self._set_new_presentation(new_presentation)
