# ruff: noqa: SLF001
import datetime

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa.common import TimeoutType

from .auth import AuthPresentation
from .home import HomePresentation
from .login import LoginPresentation
from .match import MatchPresentation
from .match.state import MatchState
from .presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)
from .room import RoomOwnerPresentation


class PresentationCreator(PresentationCreatorBase):
    @staticmethod
    def wait(
        browser: BrowserBase,
        timeout: TimeoutType,
        presentation: Presentation,
    ) -> None:
        match presentation:
            case Presentation.LOGIN:
                LoginPresentation._wait(browser, timeout)
            case Presentation.AUTH:
                AuthPresentation._wait(browser, timeout)
            case Presentation.HOME:
                HomePresentation._wait(browser, timeout)
            case Presentation.TOURNAMENT:
                raise NotImplementedError
            case Presentation.ROOMOWNER:
                RoomOwnerPresentation._wait(browser, timeout)
            case Presentation.MATCH:
                MatchPresentation._wait(browser, timeout)
            case _:
                raise AssertionError

    def create_new_presentation(  # noqa: PLR0911
        self,
        current_presentation: Presentation,
        next_presentation: Presentation,
        browser: BrowserBase,
        db_client: DBClientBase,
        **kwargs,
    ) -> PresentationBase:
        match next_presentation:
            case Presentation.LOGIN:
                return LoginPresentation(browser, db_client, self)
            case Presentation.AUTH:
                return AuthPresentation(browser, db_client, self)
            case Presentation.HOME:
                if not isinstance(
                    kwargs.get("timeout"),
                    int | float | datetime.timedelta,
                ):
                    raise TypeError
                return HomePresentation(
                    browser,
                    db_client,
                    self,
                    kwargs["timeout"],
                )
            case Presentation.TOURNAMENT:
                raise NotImplementedError
            case Presentation.ROOMOWNER:
                match current_presentation:
                    case Presentation.HOME | Presentation.MATCH:
                        if not isinstance(
                            kwargs.get("timeout"),
                            int | float | datetime.timedelta,
                        ):
                            raise TypeError
                        return RoomOwnerPresentation._create(
                            browser,
                            db_client,
                            self,
                            kwargs["timeout"],
                        )
                    case _:
                        raise NotImplementedError
            case Presentation.MATCH:
                if not isinstance(
                    kwargs.get("timeout"),
                    int | float | datetime.timedelta,
                ):
                    raise TypeError
                match current_presentation:
                    case Presentation.AUTH:
                        # TODO: What to do when a suspended match is resumed.
                        return MatchPresentation(
                            browser,
                            db_client,
                            self,
                            current_presentation,
                            kwargs["timeout"],
                        )
                    case Presentation.ROOMOWNER:
                        return MatchPresentation(
                            browser,
                            db_client,
                            self,
                            current_presentation,
                            kwargs["timeout"],
                        )
                    case Presentation.MATCH:
                        if not isinstance(
                            kwargs.get("match_state"),
                            MatchState,
                        ):
                            raise TypeError
                        return MatchPresentation(
                            browser,
                            db_client,
                            self,
                            current_presentation,
                            kwargs["timeout"],
                            match_state=kwargs["match_state"],
                        )
                    case _:
                        raise NotImplementedError
            case _:
                raise AssertionError
