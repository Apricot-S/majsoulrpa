from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from majsoulrpa.screens.match.screen import MatchScreen

__all__ = ["MatchScreen"]


def __getattr__(name: str) -> object:
    if name != "MatchScreen":
        msg = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)

    from majsoulrpa.screens.match.screen import MatchScreen  # noqa: PLC0415

    globals()[name] = MatchScreen
    return MatchScreen
