from typing import ClassVar


class ScreenDetectionSpec:
    pass


class Screen:
    detection: ClassVar[ScreenDetectionSpec | None] = None

    @classmethod
    def detection_spec(cls) -> ScreenDetectionSpec | None:
        return cls.detection
