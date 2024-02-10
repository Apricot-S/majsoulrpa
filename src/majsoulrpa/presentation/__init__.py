"""Provides presentation classes.

In this context, a *presentation* refers to a specific screen state of
the game. Each presentation acts as both the View and Controller in the
MVC (Model-View-Controller) pattern. As the View, it is tasked with
detecting and recognizing the screen state. As the Controller, it
manages interactions with widgets on the screen.
"""

from .auth import AuthPresentation
from .home import HomePresentation, JoinRoomFailureReason
from .login import LoginPresentation
from .presentation_base import (
    BaseError,
    BrowserRefreshRequest,
    InconsistentMessageError,
    InvalidOperationError,
    NotImplementedOperationError,
    PresentationBase,
    PresentationNotDetectedError,
    PresentationTimeoutError,
    UnexpectedStateError,
)
from .room import RoomGuestPresentation, RoomHostPresentation

__all__ = [
    "BaseError",
    "BrowserRefreshRequest",
    "InconsistentMessageError",
    "InvalidOperationError",
    "NotImplementedOperationError",
    "PresentationNotDetectedError",
    "PresentationTimeoutError",
    "UnexpectedStateError",
    "PresentationBase",
    "LoginPresentation",
    "AuthPresentation",
    "HomePresentation",
    "JoinRoomFailureReason",
    "RoomHostPresentation",
    "RoomGuestPresentation",
]
