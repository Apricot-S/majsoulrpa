import datetime
from collections.abc import Iterable, Mapping
from logging import getLogger
from typing import Self, Union

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline
from majsoulrpa.presentation.presentation_base import (
    InconsistentMessage,
    Presentation,
    PresentationCreatorBase,
    PresentationNotDetected,
    Timeout,
    UnexpectedState,
)

from . import host
from .base import RoomPlayer, RoomPresentationBase

logger = getLogger(__name__)


class RoomGuestPresentation(RoomPresentationBase):
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
        super().__init__(
            browser,
            db_client,
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
        db_client: DBClientBase,
        creator: PresentationCreatorBase,
        timeout: TimeoutType,
    ) -> Union[Self, "host.RoomHostPresentation"]:
        deadline = timeout_to_deadline(timeout)

        template = Template.open_file(
            "template/room/marker",
            browser.zoom_ratio,
        )
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
                case ".lq.Lobby.joinRoom" | ".lq.Lobby.fetchRoom":
                    logger.info(message)
                    break
                case ".lq.NotifyRoomPlayerUpdate":
                    # Sometimes '.lq.NotifyRoomPlayerUpdate'
                    # is sent before .lq.Lobby.joinRoom.
                    logger.info(message)
                    continue

            raise InconsistentMessage(str(message), sct)

        if not isinstance(response, Mapping):
            msg = f"'{name}' response does not have a dict."
            raise InconsistentMessage(msg, None)

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
            db_client,
            creator,
            room_id,
            max_num_players,
            players,
            num_ais,
        )

    @classmethod
    def _return_from_match(  # noqa: PLR0913
        cls,
        browser: BrowserBase,
        db_client: DBClientBase,
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
                raise Timeout(msg, browser.get_screenshot())

            now = datetime.datetime.now(datetime.UTC)
            message = db_client.dequeue_message(deadline - now)
            if message is None:
                break
            _, name, _, _, _ = message

            match name:
                case ".lq.Lobby.heatbeat" | ".lq.FastTest.checkNetworkDelay":
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

            raise InconsistentMessage(str(message), browser.get_screenshot())

        add_ai = Template.open_file(
            "template/room/add_ai",
            browser.zoom_ratio,
        )
        if add_ai.match(browser.get_screenshot()):
            return host.RoomHostPresentation(
                browser,
                db_client,
                creator,
                prev_presentation.room_id,
                prev_presentation.max_num_players,
                prev_presentation.players,
                prev_presentation.num_ais,
            )

        return cls(
            browser,
            db_client,
            creator,
            prev_presentation.room_id,
            prev_presentation.max_num_players,
            prev_presentation.players,
            prev_presentation.num_ais,
        )

    def ready(self, timeout: TimeoutType = 60.0) -> None:
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
                if p.account_id == self._db_client.account_id
            ),
            -1,
        )
        if own_player_index == -1:
            msg = "Own player is not included in the player list."
            raise UnexpectedState(msg, self._browser.get_screenshot())

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
        except Timeout:
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
                Presentation.ROOMGUEST,
                Presentation.MATCH,
                self._browser,
                self._db_client,
                timeout=(deadline - now),
            )
            self._set_new_presentation(new_presentation)
