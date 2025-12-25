from enum import Enum, auto


class Mode(Enum):
    FOUR_PLAYER = auto()
    THREE_PLAYER = auto()


class Length(Enum):
    ONE_GAME = auto()
    EAST_ONLY = auto()
    TWO_WIND_MATCH = auto()
    VS_AI = auto()


class ThinkingTime(Enum):
    THREE_PLUS_FIVE = auto()
    FIVE_PLUS_TEN = auto()
    FIVE_PLUS_TWENTY = auto()
    SIXTY_PLUS_ZERO = auto()
    THREE_HUNDRED_PLUS_ZERO = auto()
