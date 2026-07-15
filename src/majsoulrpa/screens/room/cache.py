from dataclasses import replace

from pydantic import JsonValue

from majsoulrpa.screens.room._decode import (
    RoomStateDecodeError,
    decode_room_state,
)
from majsoulrpa.screens.room.state import RoomPlayer, RoomState, RoomStatus
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
)

_FULL_SNAPSHOT_API_NAMES = frozenset(
    {
        ".lq.Lobby.createRoom",
        ".lq.Lobby.fetchRoom",
        ".lq.Lobby.joinRoom",
    },
)
_TERMINAL_NOTICE_STATUSES = {
    ".lq.NotifyRoomGameStart": RoomStatus.MATCH_STARTED,
    ".lq.NotifyRoomKickOut": RoomStatus.KICKED,
}


class RoomStateTransitionError(ValueError):
    """Raised when room messages describe an invalid transition."""


class RoomStateCache:
    def __init__(self) -> None:
        self._state: RoomState | None = None
        self._generation = 0

    @property
    def state(self) -> RoomState | None:
        return self._state

    @property
    def generation(self) -> int:
        return self._generation

    def apply(
        self,
        message: DecodedSnifferMessage,
        self_account_id: int,
    ) -> RoomState | None:
        if isinstance(message, DecodedNotice):
            return self._apply_notice(message, self_account_id)
        return self._apply_request_response(message, self_account_id)

    def _apply_notice(
        self,
        message: DecodedNotice,
        self_account_id: int,
    ) -> RoomState | None:
        status = _TERMINAL_NOTICE_STATUSES.get(message.raw.name)
        if status is not None:
            return self._apply_terminal(status)
        if message.raw.name == ".lq.NotifyRoomPlayerUpdate":
            return self._apply_player_update(message.message, self_account_id)
        if message.raw.name == ".lq.NotifyRoomPlayerReady":
            return self._apply_ready_update(message.message)
        return self._state

    def _apply_request_response(
        self,
        message: DecodedRequestResponse,
        self_account_id: int,
    ) -> RoomState | None:
        if message.raw.name == ".lq.Lobby.leaveRoom":
            if "error" in message.response:
                return self._state
            return self._apply_terminal(RoomStatus.LEFT)
        if message.raw.name not in _FULL_SNAPSHOT_API_NAMES:
            return self._state
        return self._apply_full_snapshot(message.response, self_account_id)

    def _apply_full_snapshot(
        self,
        response: dict[str, JsonValue],
        self_account_id: int,
    ) -> RoomState | None:
        if "error" in response:
            return self._state

        room = response.get("room")
        if not isinstance(room, dict):
            msg = "A successful room response must contain a room object."
            raise RoomStateDecodeError(msg)

        previous = self._state
        version = 1 if previous is None else previous.version + 1
        state = decode_room_state(
            room,
            version=version,
            self_account_id=self_account_id,
        )

        if previous is not None and previous.status is RoomStatus.WAITING:
            if previous.room_id != state.room_id:
                msg = "An active room generation cannot change room ID."
                raise RoomStateTransitionError(msg)
            if replace(state, version=previous.version) == previous:
                return previous

        if previous is None or previous.status is not RoomStatus.WAITING:
            self._generation += 1

        self._state = state
        return state

    def _apply_terminal(self, status: RoomStatus) -> RoomState:
        previous = self._state
        if previous is None:
            msg = "A room cannot become terminal before its initial snapshot."
            raise RoomStateTransitionError(msg)
        if previous.status is not RoomStatus.WAITING:
            return previous

        state = replace(
            previous,
            version=previous.version + 1,
            status=status,
        )
        self._state = state
        return state

    def _apply_player_update(
        self,
        message: dict[str, JsonValue],
        self_account_id: int,
    ) -> RoomState:
        previous = self._require_state_for_update()
        if previous.status is not RoomStatus.WAITING:
            return previous

        player_list = message.get("player_list")
        updated_account_ids: set[int] = set()
        if isinstance(player_list, list):
            for value in player_list:
                if not isinstance(value, dict):
                    continue
                account_id = value.get("account_id")
                if isinstance(account_id, bool) or not isinstance(
                    account_id,
                    int,
                ):
                    continue
                updated_account_ids.add(account_id)

        current_account_ids = {
            player.account_id
            for player in previous.players
            if player.is_ready and player.account_id in updated_account_ids
        }
        room: dict[str, JsonValue] = {
            "room_id": previous.room_id,
            "owner_id": message.get("owner_id"),
            "max_player_count": previous.max_player_count,
            "persons": player_list,
            "ready_list": list(current_account_ids),
            "robot_count": message.get("robot_count"),
        }
        state = decode_room_state(
            room,
            version=previous.version + 1,
            self_account_id=self_account_id,
        )
        if replace(state, version=previous.version) == previous:
            return previous
        self._state = state
        return state

    def _apply_ready_update(self, message: dict[str, JsonValue]) -> RoomState:
        previous = self._require_state_for_update()
        if previous.status is not RoomStatus.WAITING:
            return previous

        account_id = message.get("account_id")
        if (
            isinstance(account_id, bool)
            or not isinstance(account_id, int)
            or account_id <= 0
        ):
            msg = "room ready account_id must be a positive integer."
            raise RoomStateDecodeError(msg)
        ready = message.get("ready")
        if not isinstance(ready, bool):
            msg = "room ready value must be a boolean."
            raise RoomStateDecodeError(msg)

        players: list[RoomPlayer] = []
        found = False
        for player in previous.players:
            if player.account_id != account_id:
                players.append(player)
                continue
            found = True
            players.append(replace(player, is_ready=ready))
        if not found:
            msg = "room ready account_id must identify a room player."
            raise RoomStateDecodeError(msg)

        player_tuple = tuple(players)
        if player_tuple == previous.players:
            return previous
        state = replace(
            previous,
            version=previous.version + 1,
            players=player_tuple,
        )
        self._state = state
        return state

    def _require_state_for_update(self) -> RoomState:
        state = self._state
        if state is None:
            msg = "A room update requires an initial snapshot."
            raise RoomStateTransitionError(msg)
        return state
