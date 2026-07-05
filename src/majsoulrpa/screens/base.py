from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field


def _never_matches(_screenshot: object) -> bool:
    return False


@dataclass(frozen=True)
class ScreenDetectionSpec:
    predicate: Callable[[object], bool] = field(default=_never_matches)

    def matches(self, screenshot: object) -> bool:
        return self.predicate(screenshot)


class Screen(ABC):
    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
