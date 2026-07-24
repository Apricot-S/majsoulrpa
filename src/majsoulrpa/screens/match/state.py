from dataclasses import dataclass
from enum import StrEnum
from typing import final

from majsoulrpa.screens.match.event import MatchEvent
from majsoulrpa.screens.match.operation import OperationCandidates
from majsoulrpa.screens.match.types import Seat, Tile

_CPU_LEVEL4_ID = 10101  # 初心1
_CPU_LEVEL3_ID = 20101  # 初心1


class MatchOrigin(StrEnum):
    FRIENDLY = "friendly"
    TOURNAMENT = "tournament"


@dataclass(frozen=True, slots=True)
class MatchRank:
    id: int
    score: int

    def __post_init__(self) -> None:
        if self.id <= 0:
            msg = "Match rank ID must be positive."
            raise ValueError(msg)
        if self.score < 0:
            msg = "Match rank score must be nonnegative."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class MatchPlayer:
    seat: Seat
    account_id: int
    name: str
    level4: MatchRank
    level3: MatchRank

    def __post_init__(self) -> None:
        if self.account_id <= 0:
            msg = "Match player account ID must be positive."
            raise ValueError(msg)
        if not self.name and (
            self.level4.id != _CPU_LEVEL4_ID
            or self.level4.score != 0
            or self.level3.id != _CPU_LEVEL3_ID
            or self.level3.score != 0
        ):
            msg = "A CPU match player must use the displayed beginner ranks."
            raise ValueError(msg)

    @property
    def is_cpu(self) -> bool:
        return self.name == ""


@final
@dataclass(frozen=True, slots=True)
class Dapai:
    tile: Tile
    moqie: bool
    liqi: bool
    wliqi: bool

    def __post_init__(self) -> None:
        if self.liqi and self.wliqi:
            msg = "liqi and wliqi must not both be true."
            raise ValueError(msg)


@final
@dataclass(frozen=True, slots=True)
class Chi:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Peng:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Daminggang:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Angang:
    consumed: tuple[Tile, Tile, Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Jiagang:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    added: Tile


type Fulu = Chi | Peng | Daminggang | Angang | Jiagang


@final
@dataclass(frozen=True, slots=True)
class Babei:
    moqie: bool


@dataclass(frozen=True, slots=True)
class RoundState:
    generation: int
    step: int
    chang: int
    ju: Seat
    ben: int
    liqibang: int
    dora_indicators: tuple[Tile, ...]
    left_tile_count: int
    scores: tuple[int, ...]
    shoupai: tuple[Tile, ...]
    zimopai: Tile | None
    he: tuple[tuple[Dapai, ...], ...]
    fulu: tuple[tuple[Fulu, ...], ...]
    babei: tuple[tuple[Babei, ...], ...]
    liqi: tuple[bool, ...]
    wliqi: tuple[bool, ...]
    first_draw: tuple[bool, ...]
    yifa: tuple[bool, ...]
    lingshang_zimo: tuple[bool, ...]
    previous_dapai: tuple[Seat, Tile] | None
    previous_qianggang: tuple[Seat, Tile] | None
    operation_candidates: OperationCandidates | None
    events: tuple[MatchEvent, ...]

    def __post_init__(self) -> None:
        if self.generation <= 0:
            msg = "Round generation must be positive."
            raise ValueError(msg)
        if self.step < 0:
            msg = "Round step must be nonnegative."
            raise ValueError(msg)
        if not self.events or self.events[-1].action_step != self.step:
            msg = "Round step must match the final event."
            raise ValueError(msg)
        player_count = len(self.scores)
        collections = (
            self.he,
            self.fulu,
            self.babei,
            self.liqi,
            self.wliqi,
            self.first_draw,
            self.yifa,
            self.lingshang_zimo,
        )
        if player_count not in (3, 4) or any(
            len(collection) != player_count for collection in collections
        ):
            msg = "Round seat collections must contain three or four values."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class MatchState:
    version: int
    match_id: str
    origin: MatchOrigin
    origin_id: int
    self_seat: Seat
    players: tuple[MatchPlayer, ...]
    round: RoundState

    def __post_init__(self) -> None:
        if self.version <= 0:
            msg = "Match state version must be positive."
            raise ValueError(msg)
        if not self.match_id:
            msg = "Match ID must not be empty."
            raise ValueError(msg)
        if self.origin_id <= 0:
            msg = "Match origin ID must be positive."
            raise ValueError(msg)
        if len(self.players) not in (3, 4):
            msg = "A match must contain three or four players."
            raise ValueError(msg)
        if tuple(player.seat for player in self.players) != tuple(
            range(len(self.players)),
        ):
            msg = "Match players must be ordered by seat."
            raise ValueError(msg)
        account_ids = tuple(player.account_id for player in self.players)
        if len(account_ids) != len(set(account_ids)):
            msg = "Match player account IDs must be unique."
            raise ValueError(msg)
        if not 0 <= self.self_seat < len(self.players):
            msg = "Self seat must identify a match player."
            raise ValueError(msg)
        if len(self.round.scores) != len(self.players):
            msg = "Match players and round scores must have equal lengths."
            raise ValueError(msg)
