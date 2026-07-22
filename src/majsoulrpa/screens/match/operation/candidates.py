from dataclasses import dataclass
from typing import final

from majsoulrpa.screens.match.operation.chi import ChiOperation
from majsoulrpa.screens.match.operation.daminggang import DaminggangOperation
from majsoulrpa.screens.match.operation.dapai import DapaiOperation
from majsoulrpa.screens.match.operation.liqi import LiqiOperation
from majsoulrpa.screens.match.operation.peng import PengOperation

type MatchOperation = (
    DapaiOperation
    | ChiOperation
    | PengOperation
    | DaminggangOperation
    | LiqiOperation
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class OperationCandidates:
    time_fixed_ms: int
    time_add_ms: int
    operations: tuple[MatchOperation, ...]

    def __post_init__(self) -> None:
        if self.time_fixed_ms < 0 or self.time_add_ms < 0:
            msg = "Operation time must be nonnegative."
            raise ValueError(msg)
        if not self.operations:
            msg = "Operation candidates must not be empty."
            raise ValueError(msg)
