from dataclasses import dataclass
from enum import StrEnum


class RoomStatus(StrEnum):
    WAITING = "waiting"
    MATCH_STARTED = "match_started"
    LEFT = "left"
    KICKED = "kicked"


@dataclass(frozen=True, slots=True)
class RoomPlayer:
    account_id: int
    name: str
    is_host: bool
    is_ready: bool

    def __post_init__(self) -> None:
        if self.account_id <= 0:
            msg = "Room player account ID must be positive."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class RoomState:
    version: int
    status: RoomStatus
    room_id: int
    max_player_count: int
    players: tuple[RoomPlayer, ...]
    ai_count: int
    self_account_id: int

    def __post_init__(self) -> None:
        if self.version <= 0:
            msg = "Room state version must be positive."
            raise ValueError(msg)
        if self.room_id <= 0:
            msg = "Room ID must be positive."
            raise ValueError(msg)
        if self.max_player_count not in {3, 4}:
            msg = "Room maximum player count must be 3 or 4."
            raise ValueError(msg)
        if self.ai_count < 0:
            msg = "Room AI count must not be negative."
            raise ValueError(msg)
        if self.self_account_id <= 0:
            msg = "Self account ID must be positive."
            raise ValueError(msg)

        account_ids = [player.account_id for player in self.players]
        if len(account_ids) != len(set(account_ids)):
            msg = "Room player account IDs must be unique."
            raise ValueError(msg)
        if self.self_account_id not in account_ids:
            msg = "Self account ID must identify a room player."
            raise ValueError(msg)
        if sum(player.is_host for player in self.players) != 1:
            msg = "A room must have exactly one host player."
            raise ValueError(msg)
        if self.participant_count > self.max_player_count:
            msg = "Room participants must not exceed the maximum."
            raise ValueError(msg)

    @property
    def self_is_host(self) -> bool:
        return next(
            player.is_host
            for player in self.players
            if player.account_id == self.self_account_id
        )

    @property
    def self_is_ready(self) -> bool:
        return next(
            player.is_ready
            for player in self.players
            if player.account_id == self.self_account_id
        )

    @property
    def all_guests_ready(self) -> bool:
        return all(
            player.is_ready for player in self.players if not player.is_host
        )

    @property
    def participant_count(self) -> int:
        return len(self.players) + self.ai_count

    @property
    def available_slots(self) -> int:
        return self.max_player_count - self.participant_count
