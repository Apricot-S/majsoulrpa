import datetime
import platform
import uuid
from logging import getLogger
from pathlib import Path
from subprocess import Popen
from typing import Final, Self

if platform.system() == "Windows":
    from subprocess import CREATE_NEW_CONSOLE

from ._impl.browser import BrowserBase, DesktopBrowser
from ._impl.db_client import DBClient, DBClientBase
from .presentation import AuthPresentation, HomePresentation, LoginPresentation
from .presentation.presentation_base import (
    PresentationBase,
    PresentationNotDetected,
    Timeout,
)
from .presentation.presentation_creator import PresentationCreator

logger = getLogger(__name__)

_SERVER_PATH: Final = Path(__file__).parent / "_impl/db_server.py"
_SNIFFER_PATH: Final = Path(__file__).parent / "_mitmproxy/sniffer.py"

class RPA:

    def __init__(  # noqa: PLR0913
        self, proxy_port: int | None = 8080, db_port: int | None = 37247,
        initial_left: int = 0, initial_top: int = 0,
        viewport_height: int = 1080,
    ) -> None:
        self._id = uuid.uuid4()
        self._proxy_port = proxy_port
        self._db_port = db_port
        self._initial_left = initial_left
        self._initial_top = initial_top
        self._viewport_height = viewport_height

        self._db_process: Popen[bytes] | None = None
        self._mitmproxy_process: Popen[bytes] | None = None
        self._browser: BrowserBase | None = None
        self._db_client: DBClientBase | None = None
        self._creator = PresentationCreator()

    def __enter__(self) -> Self:
        # Run DB server process
        server_args: list[str | Path] = []
        if self._proxy_port is None:
            server_args = ["py", _SERVER_PATH]
        else:
            server_args = ["py", _SERVER_PATH, "--port", f"{self._db_port}"]

        match platform.system():
            case "Windows":
                self._db_process = Popen(
                    server_args, creationflags=CREATE_NEW_CONSOLE,  # noqa: S603
                )
            case "Linux":
                raise NotImplementedError
            case _:
                raise NotImplementedError

        # Run network sniffering process
        sniffer_args: list[str | Path] = []
        if self._proxy_port is None:
            sniffer_args = ["mitmdump", "-s", _SNIFFER_PATH]
        else:
            sniffer_args = [
                "mitmdump", "-s", _SNIFFER_PATH, "-p", f"{self._proxy_port}",
            ]

        match platform.system():
            case "Windows":
                self._mitmproxy_process = Popen(
                    sniffer_args, creationflags=CREATE_NEW_CONSOLE,  # noqa: S603
                )
            case "Linux":
                raise NotImplementedError
            case _:
                raise NotImplementedError

        # Construct a class instance that abstracts browser operations
        if self._proxy_port is None:
            self._browser = None
        else:
            self._browser = DesktopBrowser(
                proxy_port=self._proxy_port,
                initial_left=self._initial_left,
                initial_top=self._initial_top,
                width=self._viewport_height * 16 // 9,
                height=self._viewport_height,
            )

        # Construct a class instance that abstracts DB client
        if self._db_port is None:
            self._db_client = DBClient()
        else:
            self._db_client = DBClient("localhost", self._db_port)

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        self._db_client = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._mitmproxy_process is not None:
            if self._mitmproxy_process.poll() is None:
                self._mitmproxy_process.kill()
            self._mitmproxy_process = None
        if self._db_process is not None:
            if self._db_process.poll() is None:
                self._db_process.kill()
            self._db_process = None

    def get_account_id(self) -> int:
        if self._db_client is None:
            msg = "DB client has not been launched yet."
            raise RuntimeError(msg)
        if self._db_client.account_id is None:
            msg = "'account_id' has not been fetched yet."
            raise RuntimeError(msg)
        return self._db_client.account_id

    def get_screenshot(self) -> bytes:
        if self._browser is None:
            msg = "Browser has not been launched yet."
            raise RuntimeError(msg)
        return self._browser.get_screenshot()

    def activate_browser(self) -> None:
        pass

    def wait(self, timeout: float) -> PresentationBase:  # noqa: PLR0912, C901
        start_time = datetime.datetime.now(datetime.UTC)
        deadline = start_time + datetime.timedelta(seconds=timeout)

        if self._browser is None:
            msg = "Browser has not been launched yet."
            raise RuntimeError(msg)
        if self._db_client is None:
            msg = "DB client has not been launched yet."
            raise RuntimeError(msg)

        p: PresentationBase | None = None
        while True:
            try:
                p = LoginPresentation(
                    self._browser, self._db_client, self._creator,
                )
            except PresentationNotDetected:
                pass
            else:
                return p

            try:
                p = AuthPresentation(
                    self._browser, self._db_client, self._creator,
                )
            except PresentationNotDetected:
                pass
            else:
                return p

            try:
                # If it have transitioned to 'HomePresentation'
                # and any announcements are displayed, close them.
                now = datetime.datetime.now(datetime.UTC)
                HomePresentation._close_notifications(  # noqa: SLF001
                    self._browser, deadline - now,
                )
                now = datetime.datetime.now(datetime.UTC)
                p = HomePresentation(
                    self._browser, self._db_client, self._creator,
                    deadline - now,
                )
            except PresentationNotDetected:
                pass
            else:
                return p

            now = datetime.datetime.now(datetime.UTC)
            if now > deadline:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())
