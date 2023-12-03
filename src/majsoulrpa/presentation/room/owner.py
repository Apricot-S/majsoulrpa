import contextlib
import datetime
import time
from collections.abc import Iterable, Mapping
from logging import getLogger
from typing import Self

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType
from majsoulrpa.presentation.presentation_base import (
    InconsistentMessage,
    InvalidOperation,
    PresentationCreatorBase,
    PresentationNotDetected,
    PresentationNotUpdated,
    Timeout,
)

from .base import RoomPlayer, RoomPresentationBase

logger = getLogger(__name__)


class RoomOwnerPresentation(RoomPresentationBase):

    def __init__(  # noqa: PLR0913
        self, browser: BrowserBase, db_client: DBClientBase,
        creator: PresentationCreatorBase,
        room_id: int, max_num_players: int,
        players: Iterable[RoomPlayer], num_ais: int,
    ) -> None:
        super().__init__(
            browser, db_client, creator,
            room_id, max_num_players, players, num_ais,
        )

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 60.0) -> None:
        template = Template.open_file("template/room/marker",
                                      browser.zoom_ratio)
        template.wait_for(browser, timeout)

    @classmethod
    def _create(
        cls, browser: BrowserBase, db_client: DBClientBase,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> Self:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        template = Template.open_file("template/room/marker",
                                      browser.zoom_ratio)
        sct = browser.get_screenshot()
        if not template.match(sct):
            msg = "Could not detect 'room'."
            raise PresentationNotDetected(msg, sct)

        while True:
            now = datetime.datetime.now(datetime.UTC)
            message = db_client.dequeue_message(deadline - now)
            if message is None:
                msg = "Timeout."
                raise Timeout(msg, sct)
            _, name, _, response, _ = message

            match name:
                case (".lq.Lobby.createRoom"
                      | ".lq.Lobby.fetchRoom"):
                    logger.info(message)
                    break

            raise InconsistentMessage(str(message), sct)

        if not isinstance(response, Mapping):
            msg = f"'{name}' response does not have a dict."
            raise InconsistentMessage(msg, None)

        room: dict = response["room"]
        room_id: int = room["room_id"]
        owner_id: int = room["owner_id"]
        if owner_id != db_client.account_id:
            raise InconsistentMessage(str(message), sct)
        max_num_players: int = room["max_player_count"]
        ready_list: list[int] = room["ready_list"]
        players: list[RoomPlayer] = []
        for person in room["persons"]:
            account_id = person["account_id"]
            player = RoomPlayer(
                account_id, person["nickname"],
                is_host=(account_id == owner_id),
                is_ready=(account_id in ready_list),
            )
            players.append(player)
        num_ais = room["robot_count"]

        return cls(
            browser, db_client, creator,
            room_id, max_num_players, players, num_ais,
        )

    @classmethod
    def _return_from_match(  # noqa: PLR0913
        cls, browser: BrowserBase, db_client: DBClientBase,
        creator: PresentationCreatorBase,
        prev_presentation: Self, timeout: TimeoutType,
    ) -> Self:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        now = datetime.datetime.now(datetime.UTC)
        cls._wait(browser, deadline - now)

        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, browser.get_screenshot())

            now = datetime.datetime.now(datetime.UTC)
            message = db_client.dequeue_message(deadline - now)
            if message is None:
                break
            direction, name, request, response, timestamp = message

            match name:
                case (".lq.Lobby.heatbeat"
                      | ".lq.FastTest.checkNetworkDelay"):
                    continue
                case ".lq.Lobby.fetchAccountInfo":
                    # TODO(Apricot-S): Update account information  # noqa: TD003, E501
                    continue
                case ".lq.Lobby.fetchRoom":
                    # TODO(Apricot-S): Update of room information  # noqa: TD003, E501
                    continue

            raise InconsistentMessage(name, browser.get_screenshot())

        return cls(
            browser, db_client, creator,
            prev_presentation.room_id, prev_presentation.max_num_players,
            prev_presentation.players, prev_presentation.num_ais,
        )

    def _update(self, timeout: TimeoutType) -> bool:
        self._assert_not_stale()

        if not (result := super()._update(timeout)):
            msg = "'room_host' has not been updated yet."
            raise PresentationNotUpdated(msg, None)
        return result

    def add_ai(self, timeout: TimeoutType = 10.0) -> None:
        self._assert_not_stale()

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        # Check if you can click "Add AI".
        template = Template.open_file("template/room/add_ai",
                                      self._browser.zoom_ratio)
        sct = self._browser.get_screenshot()
        if not template.match(sct):
            msg = "Could not add AI."
            raise InvalidOperation(msg, sct)

        old_num_ais = self.num_ais

        # Click "Add AI".
        template.click(self._browser)
        # An effect occurs when you click "Add AI" and
        # the effect interferes with template matching
        # when you click "Add AI" consecutively,
        # so wait until the effect disappears.
        time.sleep(2.0)

        # Wait until WebSocket messages come in and
        # the number of AIs actually increases.
        while self.num_ais <= old_num_ais:
            now = datetime.datetime.now(datetime.UTC)
            with contextlib.suppress(PresentationNotDetected):
                self._update(deadline - now)

    def start(self, timeout: TimeoutType = 60.0) -> None:
        self._assert_not_stale()

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        template = Template.open_file("template/room/start",
                                      self._browser.zoom_ratio)
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())
            if template.match(self._browser.get_screenshot()):
                break
        template.click(self._browser)
