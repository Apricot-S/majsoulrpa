from dataclasses import dataclass
from enum import StrEnum

from majsoulrpa.screens.match.event import MatchEvent

_MAX_PLAYER_COUNT = 4


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
    seat: int
    account_id: int | None
    name: str | None
    level4: MatchRank | None
    level3: MatchRank | None

    def __post_init__(self) -> None:
        if not 0 <= self.seat < _MAX_PLAYER_COUNT:
            msg = "Match player seat must be between 0 and 3."
            raise ValueError(msg)
        if self.account_id is None:
            return
        if self.account_id <= 0:
            msg = "Match player account ID must be positive or None."
            raise ValueError(msg)
        if self.name is None or self.level4 is None or self.level3 is None:
            msg = "A human match player must have a name and both ranks."
            raise ValueError(msg)

    @property
    def is_cpu(self) -> bool:
        return self.account_id is None


@dataclass(frozen=True, slots=True)
class MatchDapai:
    tile: str
    moqie: bool
    liqi: bool
    wliqi: bool


class MatchFuluKind(StrEnum):
    CHI = "chi"
    PENG = "peng"
    DAMINGGANG = "daminggang"
    ANGANG = "angang"
    JIAGANG = "jiagang"


@dataclass(frozen=True, slots=True)
class MatchFulu:
    kind: MatchFuluKind
    tiles: tuple[str, ...]
    from_seat: int | None


@dataclass(frozen=True, slots=True)
class RoundState:
    generation: int
    step: int
    chang: int
    ju: int
    ben: int
    liqibang: int
    dora_indicators: tuple[str, ...]
    left_tile_count: int
    scores: tuple[int, ...]
    shoupai: tuple[str, ...]
    zimopai: str | None
    he: tuple[tuple[MatchDapai, ...], ...]
    fulu: tuple[tuple[MatchFulu, ...], ...]
    num_babei: tuple[int, ...]
    liqi: tuple[bool, ...]
    wliqi: tuple[bool, ...]
    first_draw: tuple[bool, ...]
    yifa: tuple[bool, ...]
    lingshang_zimo: tuple[bool, ...]
    previous_dapai_seat: int | None
    previous_dapai_tile: str | None
    has_pending_operation: bool
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
            self.num_babei,
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
    self_seat: int
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
        if not 0 <= self.self_seat < len(self.players):
            msg = "Self seat must identify a match player."
            raise ValueError(msg)
        if len(self.round.scores) != len(self.players):
            msg = "Match players and round scores must have equal lengths."
            raise ValueError(msg)
