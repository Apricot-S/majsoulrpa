from abc import ABC, abstractmethod


class ScreenDetectionSpec:
    pass


class Screen(ABC):
    @classmethod
    @abstractmethod
    def detection_spec(cls) -> ScreenDetectionSpec:
        raise NotImplementedError
