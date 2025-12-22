from enum import Enum, auto


class Mode(Enum):
    FOUR_PLAYER = auto()
    THREE_PLAYER = auto()


class Length(Enum):
    ONE_GAME = auto()
    EAST_ONLY = auto()
    TWO_WIND_MATCH = auto()
    VS_AI = auto()
