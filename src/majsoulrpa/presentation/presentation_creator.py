# ruff: noqa: SLF001
import datetime

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa.common import TimeoutType

from .auth import AuthPresentation
from .home import HomePresentation
from .login import LoginPresentation
from .presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)
from .room import RoomHostPresentation


class PresentationCreator(PresentationCreatorBase):

    @staticmethod
    def wait(
        browser: BrowserBase, timeout: TimeoutType, presentation: Presentation,
    ) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        match presentation:
            case Presentation.LOGIN:
                LoginPresentation._wait(browser, timeout)
            case Presentation.AUTH:
                AuthPresentation._wait(browser, timeout)
            case Presentation.HOME:
                HomePresentation._wait(browser, timeout)
            case Presentation.TOURNAMENT:
                raise NotImplementedError
            case Presentation.ROOMHOST:
                RoomHostPresentation._wait(browser, timeout)
            case Presentation.MATCH:
                raise NotImplementedError
            case _:
                raise AssertionError

    def create_new_presentation(
        self,
        current_presentation: Presentation, next_presentation: Presentation,
        browser: BrowserBase, db_client: DBClientBase,
        **kwargs,
    ) -> "PresentationBase":
        match next_presentation:
            case Presentation.LOGIN:
                return LoginPresentation(browser, db_client, self)
            case Presentation.AUTH:
                return AuthPresentation(browser, db_client, self)
            case Presentation.HOME:
                if not isinstance(kwargs.get("timeout"),
                                  int | float | datetime.timedelta):
                    raise TypeError
                return HomePresentation(browser, db_client, self,
                                        kwargs["timeout"])
            case Presentation.TOURNAMENT:
                raise NotImplementedError
            case Presentation.ROOMHOST:
                match current_presentation:
                    case Presentation.HOME:
                        if not isinstance(kwargs.get("timeout"),
                                          int | float | datetime.timedelta):
                            raise TypeError
                        return RoomHostPresentation._create(
                            browser, db_client, self, kwargs["timeout"],
                        )
                    case _:
                        raise NotImplementedError
            case Presentation.MATCH:
                raise NotImplementedError
            case _:
                raise AssertionError
