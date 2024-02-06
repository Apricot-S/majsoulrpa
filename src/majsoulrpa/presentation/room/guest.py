import datetime
from collections.abc import Iterable, Mapping
from logging import getLogger
from typing import Self, Union

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline
from majsoulrpa.presentation.presentation_base import (
    InconsistentMessageError,
    Presentation,
    PresentationCreatorBase,
    PresentationNotDetectedError,
    PresentationTimeoutError,
    UnexpectedStateError,
)

from . import host
from .base import RoomPlayer, RoomPresentationBase

logger = getLogger(__name__)


class RoomGuestPresentation(RoomPresentationBase):
    """Room guest presentation.

    Represents the room screen as seen by a guest. Users can perform
    the following operation with an instance of `RoomGuestPresentation`:

    * Notify that the guest is ready to start the match.
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
        """Creates an instance of `RoomGuestPresentation`.

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
    def _join(
        cls,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> Union[Self, "host.RoomHostPresentation"]:
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
                case ".lq.Lobby.joinRoom" | ".lq.Lobby.fetchRoom":
                    logger.info(message)
                    break
                case ".lq.NotifyRoomPlayerUpdate":
                    # Sometimes `.lq.NotifyRoomPlayerUpdate`
                    # is sent before .lq.Lobby.joinRoom.
                    logger.info(message)
                    continue

            raise InconsistentMessageError(str(message), ss)

        if not isinstance(response, Mapping):
            msg = f"`{name}` response does not have a dict."
            raise InconsistentMessageError(msg)

        room: dict = response["room"]
        room_id: int = room["room_id"]
        owner_id: int = room["owner_id"]
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
    ) -> Union[Self, "host.RoomHostPresentation"]:
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
                    # TODO(Apricot-S): Update account information  # noqa: TD003, E501
                    logger.info(message)
                    continue
                case ".lq.Lobby.fetchRoom":
                    # TODO(Apricot-S): Update of room information  # noqa: TD003, E501
                    logger.info(message)
                    continue

            raise InconsistentMessageError(
                str(message),
                browser.get_screenshot(),
            )

        add_ai = Template.open_file(
            "template/room/add_ai",
            browser.zoom_ratio,
        )
        if add_ai.match(browser.get_screenshot()):
            return host.RoomHostPresentation(
                browser,
                message_queue_client,
                creator,
                prev_presentation.room_id,
                prev_presentation.max_num_players,
                prev_presentation.players,
                prev_presentation.num_ais,
            )

        return cls(
            browser,
            message_queue_client,
            creator,
            prev_presentation.room_id,
            prev_presentation.max_num_players,
            prev_presentation.players,
            prev_presentation.num_ais,
        )

    def ready(self, timeout: TimeoutType = 60.0) -> None:
        """Notifies that the guest is ready to start the match.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                guest to become ready. Defaults to `60.0`.

        Raises:
            UnexpectedStateError: If the guest is not included in the
                player list.
            PresentationTimeoutError: If the guest does not become
                ready within the specified timeout period.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        ready_template = Template.open_file(
            "template/room/ready",
            self._browser.zoom_ratio,
        )
        ready_template.wait_until_then_click(self._browser, deadline)

        own_player_index = next(
            (
                i
                for i, p in enumerate(self.players)
                if p.account_id == self._message_queue_client.account_id
            ),
            -1,
        )
        if own_player_index == -1:
            msg = "Own player is not included in the player list."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        while not self.players[own_player_index].is_ready:
            now = datetime.datetime.now(datetime.UTC)
            self._update(deadline - now)

        try:
            now = datetime.datetime.now(datetime.UTC)
            self._creator.wait(
                self._browser,
                deadline - now,
                Presentation.MATCH,
            )
        except PresentationTimeoutError:
            cancel_template = Template.open_file(
                "template/room/cancel",
                self._browser.zoom_ratio,
            )
            if cancel_template.click_if_match(self._browser):
                return
            raise
        else:
            now = datetime.datetime.now(datetime.UTC)
            new_presentation = self._creator.create_new_presentation(
                Presentation.ROOM_GUEST,
                Presentation.MATCH,
                self._browser,
                self._message_queue_client,
                timeout=(deadline - now),
            )
            self._set_new_presentation(new_presentation)
