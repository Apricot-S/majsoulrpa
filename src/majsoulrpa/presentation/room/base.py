from collections.abc import Iterable, Mapping

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import Player, TimeoutType
from majsoulrpa.presentation.presentation_base import (
    InconsistentMessage,
    InvalidOperation,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)


class RoomPlayer(Player):
    def __init__(
        self,
        account_id: int,
        name: str,
        *,
        is_host: bool,
        is_ready: bool,
    ) -> None:
        super().__init__(account_id, name)
        self._is_host = is_host
        self._is_ready = is_ready

    @property
    def is_host(self) -> bool:
        return self._is_host

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    def _set_ready(self, *, is_ready: bool) -> None:
        self._is_ready = is_ready


class RoomPresentationBase(PresentationBase):
    def __init__(  # noqa: PLR0913
        self,
        browser: BrowserBase,
        db_client: DBClientBase,
        creator: PresentationCreatorBase,
        room_id: int,
        max_num_players: int,
        players: Iterable[RoomPlayer],
        num_ais: int,
    ) -> None:
        super().__init__(browser, db_client, creator)

        self._room_id = room_id
        self._max_num_players = max_num_players
        self._players = list(players)
        self._num_ais = num_ais

    def _update(self, timeout: TimeoutType) -> bool:  # noqa: C901, PLR0912
        self._assert_not_stale()

        message = self._db_client.dequeue_message(timeout)
        if message is None:
            return False
        direction, name, request, response, timestamp = message

        if name == ".lq.Lobby.modifyRoom":
            return False

        if name == ".lq.NotifyRoomPlayerUpdate":
            if direction != "inbound":
                msg = "'.lq.NotifyRoomPlayerUpdate' is not inbound."
                raise InconsistentMessage(msg, None)
            if response is not None:
                msg = "'.lq.NotifyRoomPlayerUpdate' has a response."
                raise InconsistentMessage(msg, None)
            if not isinstance(request, Mapping):
                msg = "'.lq.NotifyRoomPlayerUpdate' does not have a dict."
                raise InconsistentMessage(msg, None)
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
            if direction != "inbound":
                msg = "'.lq.NotifyRoomPlayerReady' is not inbound."
                raise InconsistentMessage(msg, None)
            if response is not None:
                msg = "'.lq.NotifyRoomPlayerReady' has a response."
                raise InconsistentMessage(msg, None)
            if not isinstance(request, Mapping):
                msg = "'.lq.NotifyRoomPlayerReady' does not have a dict."
                raise InconsistentMessage(msg, None)
            account_id = request["account_id"]
            for i in range(len(self._players)):
                if self._players[i].account_id == account_id:
                    break
                if i == len(self._players):
                    msg = (
                        "An inconsistent '.lq.NotifyRoomPlayerReady' message."
                    )
                    raise InconsistentMessage(msg, None)
                self._players[i]._set_ready(is_ready=request["ready"])  # noqa: SLF001

            return True

        msg = (
            "An inconsistent message.\n"
            f"direction: {direction}\n"
            f"name: {name}\n"
            f"request: {request}\n"
            f"response: {response}\n"
            f"timestamp: {timestamp}"
        )
        raise InconsistentMessage(msg, None)

    @property
    def room_id(self) -> int:
        return self._room_id

    @property
    def max_num_players(self) -> int:
        return self._max_num_players

    @property
    def players(self) -> list[RoomPlayer]:
        return self._players

    @property
    def num_ais(self) -> int:
        return self._num_ais

    def leave(self, timeout: TimeoutType = 10.0) -> None:
        self._assert_not_stale()

        # Click on the icon to leave the room.
        template = Template.open_file(
            "template/room/leave",
            self._browser.zoom_ratio,
        )
        if not template.match(self._browser.get_screenshot()):
            msg = "Could not leave the room."
            raise InvalidOperation(msg, self._browser.get_screenshot())
        template.click(self._browser)

        # Wait until the home screen is displayed.
        self._creator.wait(self._browser, timeout, Presentation.HOME)

        new_presentation = self._creator.create_new_presentation(
            Presentation.ROOMBASE,
            Presentation.HOME,
            self._browser,
            self._db_client,
            timeout=timeout,
        )
        self._set_new_presentation(new_presentation)
