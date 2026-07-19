from typing import TYPE_CHECKING

from majsoulrpa.screens.match.event import MatchEvent, StartMatchEvent

if TYPE_CHECKING:
    from majsoulrpa.screens.match.screen import MatchScreen

__all__ = ["MatchEvent", "MatchScreen", "StartMatchEvent"]


def __getattr__(name: str) -> object:
    if name == "MatchScreen":
        from majsoulrpa.screens.match.screen import (  # noqa: PLC0415
            MatchScreen,
        )

        globals()[name] = MatchScreen
        return MatchScreen
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
