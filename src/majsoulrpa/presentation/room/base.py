from collections.abc import Iterable, Mapping
from logging import getLogger

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import Player, TimeoutType
from majsoulrpa.presentation.presentation_base import (
    InconsistentMessageError,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    UnexpectedStateError,
)

logger = getLogger(__name__)


class RoomPlayer(Player):
    """Represents a player in a room for friendly matches."""

    def __init__(
        self,
        account_id: int,
        name: str,
        *,
        is_host: bool,
        is_ready: bool,
    ) -> None:
        """Creates an instance of `RoomPlayer`.

        Args:
            account_id: The account ID of the player.
            name: The name of the player.
            is_host: `True` if the player is the host of the room;
                `False` otherwise.
            is_ready: `True` if the player is ready to start the match;
                `False` otherwise.
        """
        super().__init__(account_id, name)
        self._is_host = is_host
        self._is_ready = is_ready

    @property
    def is_host(self) -> bool:
        """Indicates whether the player is the host of the room."""
        return self._is_host

    @property
    def is_ready(self) -> bool:
        """Indicates whether the player is ready to start the match."""
        return self._is_ready

    def _set_ready(self, *, is_ready: bool) -> None:
        self._is_ready = is_ready


class RoomPresentationBase(PresentationBase):
    """Provides common functionality for room presentations."""

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
        """Creates an instance of `RoomPresentationBase`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            browser: The browser instance that is currently displaying a
                room screen.
            message_queue_client: A message queue client that is
                currently connected to the queue where mitmproxy is
                pushing messages.
            creator: A presentation creator responsible for
                instantiating presentations.
            room_id: The room ID.
            max_num_players: The maximum number of players allowed
                in the room.
            players: The players in the room.
            num_ais: The number of AI players in the room.
        """
        super().__init__(browser, message_queue_client, creator)

        self._room_id = room_id
        self._max_num_players = max_num_players
        self._players = list(players)
        self._num_ais = num_ais

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 60.0) -> None:
        template = Template.open_file(
            "template/room/marker",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def _update(self, timeout: TimeoutType) -> bool:  # noqa: C901
        self._assert_not_stale()

        message = self._message_queue_client.dequeue_message(timeout)
        if message is None:
            return False
        direction, name, request, response, timestamp = message

        if name == ".lq.Lobby.heatbeat":
            logger.info(message)
            return False

        if name == ".lq.Lobby.modifyRoom":
            logger.info(message)
            return False

        if name == ".lq.Lobby.readyPlay":
            logger.info(message)
            return False

        if name == ".lq.NotifyRoomPlayerUpdate":
            logger.info(message)
            if direction != "inbound":
                msg = "`.lq.NotifyRoomPlayerUpdate` is not inbound."
                raise InconsistentMessageError(msg)
            if response is not None:
                msg = "`.lq.NotifyRoomPlayerUpdate` has a response."
                raise InconsistentMessageError(msg)
            if not isinstance(request, Mapping):
                msg = "`.lq.NotifyRoomPlayerUpdate` does not have a dict."
                raise InconsistentMessageError(msg)
            host_account_id = request["owner_id"]
            new_players: list[RoomPlayer] = []
            for p in request["player_list"]:
                account_id = p["account_id"]
                player = RoomPlayer(
                    account_id,
                    p["nickname"],
                    is_host=(account_id == host_account_id),
                    is_ready=False,
                )
                new_players.append(player)
            self._players = new_players
            self._num_ais = request["robot_count"]

            return True

        if name == ".lq.NotifyRoomPlayerReady":
            logger.info(message)
            if direction != "inbound":
                msg = "`.lq.NotifyRoomPlayerReady` is not inbound."
                raise InconsistentMessageError(msg)
            if response is not None:
                msg = "`.lq.NotifyRoomPlayerReady` has a response."
                raise InconsistentMessageError(msg)
            if not isinstance(request, Mapping):
                msg = "`.lq.NotifyRoomPlayerReady` does not have a dict."
                raise InconsistentMessageError(msg)
            account_id = request["account_id"]
            try:
                i = next(
                    i
                    for i, player in enumerate(self._players)
                    if player.account_id == account_id
                )
            except StopIteration:
                msg = "An inconsistent `.lq.NotifyRoomPlayerReady` message."
                raise InconsistentMessageError(msg) from None
            self._players[i]._set_ready(is_ready=request["ready"])  # noqa: SLF001
            message = self._message_queue_client.dequeue_message(1.0)
            if message is not None:
                _, name, _, _, _ = message
                if name != ".lq.Lobby.readyPlay":
                    raise InconsistentMessageError(str(message))
                logger.info(message)

            return True

        msg = (
            "An inconsistent message.\n"
            f"direction: {direction}\n"
            f"name: {name}\n"
            f"request: {request}\n"
            f"response: {response}\n"
            f"timestamp: {timestamp}"
        )
        raise InconsistentMessageError(msg)

    @property
    def room_id(self) -> int:
        """The room ID."""
        return self._room_id

    @property
    def max_num_players(self) -> int:
        """The maximum number of players allowed in the room."""
        return self._max_num_players

    @property
    def players(self) -> list[RoomPlayer]:
        """The players in the room."""
        return self._players

    @property
    def num_ais(self) -> int:
        """The number of AI players in the room."""
        return self._num_ais

    def leave(self, timeout: TimeoutType = 10.0) -> None:
        """Leaves the room.

        Initiates a transition to the `HomePresentation` by clicking the
        icon to leave the room, and waits for the home screen to appear.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                home screen to appear. Defaults to `10.0`.

        Raises:
            UnexpectedStateError: Indicates that the room could not be
                left, suggesting an unexpected state was encountered.
            PresentationTimeoutError: If the home screen does not appear
                within the specified timeout period.
        """
        self._assert_not_stale()

        # Click on the icon to leave the room.
        template = Template.open_file(
            "template/room/leave",
            self._browser.zoom_ratio,
        )
        if not template.click_if_match(self._browser):
            msg = "Could not leave the room."
            raise UnexpectedStateError(msg, self._browser.get_screenshot())

        # Wait until the home screen is displayed.
        self._creator.wait(self._browser, timeout, Presentation.HOME)

        new_presentation = self._creator.create_new_presentation(
            Presentation.ROOM_BASE,
            Presentation.HOME,
            self._browser,
            self._message_queue_client,
            timeout=timeout,
        )
        self._set_new_presentation(new_presentation)
