import datetime
import uuid
from logging import getLogger
from pathlib import Path
from subprocess import Popen
from typing import TYPE_CHECKING, Any, Final, Self

from ._impl.browser import BrowserBase, DesktopBrowser, RemoteBrowser
from ._impl.zmq_client import ZMQClient
from .common import timeout_to_deadline
from .presentation import AuthPresentation, HomePresentation, LoginPresentation
from .presentation.presentation_base import (
    PresentationBase,
    PresentationNotDetected,
    Timeout,
)
from .presentation.presentation_creator import PresentationCreator

if TYPE_CHECKING:
    from ._impl.db_client import DBClientBase

logger = getLogger(__name__)

_SNIFFER_PATH: Final = Path(__file__).parent / "_mitmproxy/sniffer.py"


class RPA:
    def __init__(  # noqa: PLR0913
        self,
        *,
        remote_host: str | None = None,
        proxy_port: int = 8080,
        db_port: int | None = 37247,
        initial_left: int = 0,
        initial_top: int = 0,
        viewport_height: int = 1080,
    ) -> None:
        self._id = uuid.uuid4()
        self._remote_host = remote_host
        self._proxy_port = proxy_port
        self._db_port = db_port
        self._initial_left = initial_left
        self._initial_top = initial_top
        self._viewport_width = viewport_height * 16 // 9
        self._viewport_height = viewport_height

        self._db_process: Popen[bytes] | None = None
        self._mitmproxy_process: Popen[bytes] | None = None
        self._browser: BrowserBase | None = None
        self._db_client: DBClientBase | None = None
        self._creator = PresentationCreator()

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:  # noqa: C901, PLR0912, PLR0915
        remote_host_config = config.get("remote_host")
        match remote_host_config:
            case None:
                remote_host = None
            case str():
                remote_host = remote_host_config
            case _ as invalid_arg:
                msg = f"`remote_host` must be str: {invalid_arg}"
                raise TypeError(msg)

        port_config = config.get("port")
        if port_config is None:
            proxy_port = 8080
            db_port = 37247
        elif isinstance(port_config, dict):
            _proxy_port = port_config.get("proxy_port")
            match _proxy_port:
                case None:
                    proxy_port = 8080
                case int():
                    proxy_port = _proxy_port
                case _ as invalid_arg:
                    msg = f"`proxy_port` must be int: {invalid_arg}"
                    raise TypeError(msg)

            _db_port = port_config.get("db_port")
            match _db_port:
                case None:
                    db_port = 37247
                case "None":
                    db_port = None
                case int():
                    db_port = _db_port
                case _ as invalid_arg:
                    msg = f'`db_port` must be int or "None": {invalid_arg}'
                    raise TypeError(msg)
        else:
            msg = "`port` must be dict"
            raise TypeError(msg)

        browser_config = config.get("browser")
        if browser_config is None:
            initial_left = 0
            initial_top = 0
            viewport_height = 1080
        elif isinstance(browser_config, dict):
            _initial_position = browser_config.get("initial_position")
            if _initial_position is None:
                initial_left = 0
                initial_top = 0
            elif isinstance(_initial_position, dict):
                _left = _initial_position.get("left")
                match _left:
                    case None:
                        initial_left = 0
                    case int():
                        initial_left = _left
                    case _ as invalid_arg:
                        msg = f"`left` must be int: {invalid_arg}"
                        raise TypeError(msg)

                _top = _initial_position.get("top")
                match _top:
                    case None:
                        initial_top = 0
                    case int():
                        initial_top = _top
                    case _ as invalid_arg:
                        msg = f"`top` must be int: {invalid_arg}"
                        raise TypeError(msg)
            else:
                msg = "`initial_position` must be dict"
                raise TypeError(msg)

            _viewport_height = browser_config.get("viewport_height")
            match _viewport_height:
                case None:
                    viewport_height = 1080
                case int():
                    viewport_height = _viewport_height
                case _ as invalid_arg:
                    msg = f"`viewport_height` must be int: {invalid_arg}"
                    raise TypeError(msg)
        else:
            msg = "`browser` must be dict"
            raise TypeError(msg)

        return cls(
            remote_host=remote_host,
            proxy_port=proxy_port,
            db_port=db_port,
            initial_left=initial_left,
            initial_top=initial_top,
            viewport_height=viewport_height,
        )

    def launch(self) -> None:
        # Run network sniffering process
        if self._remote_host is None:
            sniffer_args: list[str | Path] = ["mitmdump", "-qs", _SNIFFER_PATH]
            sniffer_args.extend(["-p", f"{self._proxy_port}"])
            if self._db_port is not None:
                sniffer_args.extend(
                    ["--set", f"server_port={self._db_port + 1}"],
                )
            self._mitmproxy_process = Popen(sniffer_args)  # noqa: S603

        # Construct a class instance that abstracts browser operations
        if self._remote_host is not None:
            if self._db_port is None:
                self._browser = RemoteBrowser(
                    width=self._viewport_width,
                    height=self._viewport_height,
                )
            else:
                self._browser = RemoteBrowser(
                    db_port=self._db_port,
                    width=self._viewport_width,
                    height=self._viewport_height,
                )
        else:
            self._browser = DesktopBrowser(
                proxy_port=self._proxy_port,
                initial_left=self._initial_left,
                initial_top=self._initial_top,
                width=self._viewport_width,
                height=self._viewport_height,
            )

        # Construct a class instance that abstracts DB client
        if self._db_port is None:
            self._db_client = ZMQClient(port=37247 + 1)
        else:
            self._db_client = ZMQClient("localhost", self._db_port + 1)

    def close(self) -> None:
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

    def __enter__(self) -> Self:
        self.launch()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        self.close()

    def get_account_id(self) -> int:
        if self._db_client is None:
            msg = "DB client has not been launched yet."
            raise RuntimeError(msg)
        if self._db_client.account_id is None:
            msg = "`account_id` has not been fetched yet."
            raise RuntimeError(msg)
        return self._db_client.account_id

    def get_screenshot(self) -> bytes:
        if self._browser is None:
            msg = "Browser has not been launched yet."
            raise RuntimeError(msg)
        return self._browser.get_screenshot()

    def wait(self, timeout: float) -> PresentationBase:  # noqa: PLR0912, C901
        deadline = timeout_to_deadline(timeout)

        if self._browser is None:
            msg = "Browser has not been launched yet."
            raise RuntimeError(msg)
        if self._db_client is None:
            msg = "DB client has not been launched yet."
            raise RuntimeError(msg)

        p: PresentationBase | None = None
        while True:
            self._browser.check_single()

            try:
                p = LoginPresentation(
                    self._browser,
                    self._db_client,
                    self._creator,
                )
            except PresentationNotDetected:
                pass
            else:
                return p

            try:
                p = AuthPresentation(
                    self._browser,
                    self._db_client,
                    self._creator,
                )
            except PresentationNotDetected:
                pass
            else:
                return p

            try:
                now = datetime.datetime.now(datetime.UTC)
                p = HomePresentation(
                    self._browser,
                    self._db_client,
                    self._creator,
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
