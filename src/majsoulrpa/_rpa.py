import datetime
import uuid
from logging import getLogger
from pathlib import Path
from subprocess import Popen
from typing import TYPE_CHECKING, Any, Final, Self

from ._impl.browser import (
    ASPECT_RATIO,
    BrowserBase,
    DesktopBrowser,
    RemoteBrowser,
)
from ._impl.zmq_client import ZMQClient
from .common import timeout_to_deadline
from .presentation import AuthPresentation, HomePresentation, LoginPresentation
from .presentation._presentation_creator import PresentationCreator
from .presentation.presentation_base import (
    PresentationBase,
    PresentationNotDetectedError,
    PresentationTimeoutError,
)

if TYPE_CHECKING:
    from ._impl.message_queue_client import MessageQueueClientBase

logger = getLogger(__name__)

_SNIFFER_PATH: Final = Path(__file__).parent / "_mitmproxy/sniffer.py"


class RPA:
    """Robotic Process Automation (RPA) client class for Mahjong Soul (雀魂).

    This class has four responsibilities. The first is to manage an mitmproxy
    process that sniffs messages exchanged between the browser and the Mahjong
    Soul server. The second is to manage a browser process. The third is to
    abstract browser operations by absorbing the differences between local and
    remote browsers. The fourth is to manage a ZeroMQ client that retrieves
    messages sniffed by mitmproxy. Note that the first two responsibilities
    become those of the remote host when using a remote browser.

    Args:
        remote_host (str | None, optional): Hostname of the remote browser.
            If `None`, a local browser will be used. Defaults to `None`.
        remote_port (int, optional): Port number of the remote browser.
            Defaults to `19222`.
        proxy_port (int, optional): Port number of mitmproxy.
            Defaults to `8080`.
        message_queue_port (int | None, optional): Port number of the message
            queue server. If `None`, a local message queue server will be used.
            Defaults to `37247`.
        initial_left (int, optional): Initial left position of the browser.
            Defaults to `0`.
        initial_top (int, optional): Initial top position of the browser.
            Defaults to `0`.
        viewport_height (int, optional): Height of the viewport of the browser.
            Defaults to `1080`.
        headless (bool, optional): Whether to run the browser in headless mode.
            Defaults to `False`.
    """

    def __init__(
        self,
        *,
        remote_host: str | None = None,
        remote_port: int = 19222,
        proxy_port: int = 8080,
        message_queue_port: int | None = 37247,
        initial_left: int = 0,
        initial_top: int = 0,
        viewport_height: int = 1080,
        headless: bool = False,
    ) -> None:
        if len({remote_port, proxy_port, message_queue_port}) != 3:  # noqa: PLR2004
            msg = (
                "Ports must be different. "
                f"{remote_port=}, {proxy_port=}, {message_queue_port=}"
            )
            raise ValueError(msg)

        self._id = uuid.uuid4()
        self._remote_host = remote_host
        self._remote_port = remote_port
        self._proxy_port = proxy_port
        self._message_queue_port = message_queue_port

        self._initial_left = initial_left
        self._initial_top = initial_top
        self._viewport_width = int(viewport_height * ASPECT_RATIO)
        self._viewport_height = viewport_height
        self._headless = headless

        self._mitmproxy_process: Popen[bytes] | None = None
        self._browser: BrowserBase | None = None
        self._message_queue_client: MessageQueueClientBase | None = None
        self._creator = PresentationCreator()

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:  # noqa: C901
        """Create an instance of `RPA` from configuration.

        Args:
            config (dict[str, Any]): Configuration.

        Returns:
            Self: An instance of `RPA`.

        Raises:
            TypeError: Type of a value in `config` is incorrect.
        """
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
            remote_port = 19222
            proxy_port = 8080
            message_queue_port = 37247
        elif isinstance(port_config, dict):
            _remote_port = port_config.get("remote_port")
            match _remote_port:
                case None:
                    remote_port = 19222
                case int():
                    remote_port = _remote_port
                case _ as invalid_arg:
                    msg = f"`remote_port` must be int: {invalid_arg}"
                    raise TypeError(msg)

            _proxy_port = port_config.get("proxy_port")
            match _proxy_port:
                case None:
                    proxy_port = 8080
                case int():
                    proxy_port = _proxy_port
                case _ as invalid_arg:
                    msg = f"`proxy_port` must be int: {invalid_arg}"
                    raise TypeError(msg)

            _message_queue_port = port_config.get("message_queue_port")
            match _message_queue_port:
                case None:
                    message_queue_port = 37247
                case "None":
                    message_queue_port = None
                case int():
                    message_queue_port = _message_queue_port
                case _ as invalid_arg:
                    msg = (
                        "`message_queue_port` must be "
                        f'int or "None": {invalid_arg}'
                    )
                    raise TypeError(msg)
        else:
            msg = "`port` must be dict"
            raise TypeError(msg)

        browser_config = config.get("browser")
        if browser_config is None:
            initial_left = 0
            initial_top = 0
            viewport_height = 1080
            headless = False
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

            _headless = browser_config.get("headless")
            match _headless:
                case None:
                    headless = False
                case bool():
                    headless = _headless
                case _ as invalid_arg:
                    msg = f"`headless` must be bool: {invalid_arg}"
                    raise TypeError(msg)
        else:
            msg = "`browser` must be dict"
            raise TypeError(msg)

        return cls(
            remote_host=remote_host,
            remote_port=remote_port,
            proxy_port=proxy_port,
            message_queue_port=message_queue_port,
            initial_left=initial_left,
            initial_top=initial_top,
            viewport_height=viewport_height,
            headless=headless,
        )

    def launch(self) -> None:
        """Launch processes for RPA.

        Launch the following processes:
        - an mitmproxy process if a local browser is used,
        - a browser process if a local browser is used,
        - an abstraction layer for the browser, and
        - a ZeroMQ client.
        """
        # Run network sniffering process
        if self._remote_host is None:
            sniffer_args: list[str | Path] = [
                "mitmdump",
                "-qs",
                _SNIFFER_PATH,
                "-p",
                f"{self._proxy_port}",
            ]
            if self._message_queue_port is not None:
                sniffer_args.extend(
                    ["--set", f"port={self._message_queue_port}"],
                )
            self._mitmproxy_process = Popen(sniffer_args)  # noqa: S603

        # Construct a class instance that abstracts browser operations
        if self._remote_host is not None:
            self._browser = RemoteBrowser(self._remote_host, self._remote_port)
        else:
            self._browser = DesktopBrowser(
                self._proxy_port,
                self._initial_left,
                self._initial_top,
                self._viewport_width,
                self._viewport_height,
                headless=self._headless,
            )

        # Construct a class instance
        # that abstracts message queue client
        if self._remote_host is not None:
            if self._message_queue_port is None:
                self._message_queue_client = ZMQClient(self._remote_host)
            else:
                self._message_queue_client = ZMQClient(
                    self._remote_host,
                    self._message_queue_port,
                )
        elif self._message_queue_port is None:
            self._message_queue_client = ZMQClient()
        else:
            self._message_queue_client = ZMQClient(
                port=self._message_queue_port,
            )

    def close(self) -> None:
        """Close processes for RPA.

        Close the following processes:
        - the mitmproxy process if any,
        - the browser process if any,
        - the abstraction layer for the browser, and
        - the ZeroMQ client.
        """
        self._message_queue_client = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._mitmproxy_process is not None:
            if self._mitmproxy_process.poll() is None:
                self._mitmproxy_process.kill()
            self._mitmproxy_process = None

    def is_running(self) -> bool:
        """Check if the RPA client is running."""
        if self._message_queue_client is None:
            return False
        if self._browser is None:
            return False
        if self._remote_host is None:
            if self._mitmproxy_process is None:
                return False
            if self._mitmproxy_process.poll() is not None:
                return False
        return True

    def __enter__(self) -> Self:
        self.launch()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        self.close()

    def get_account_id(self) -> int:
        """Get the account ID of the user.

        Returns:
            int: Account ID of the user.

        Raises:
            RuntimeError: If the message queue client has not been launched
                yet.
            RuntimeError: If `account_id` has not been fetched yet.
        """
        if self._message_queue_client is None:
            msg = "Message queue client has not been launched yet."
            raise RuntimeError(msg)
        if self._message_queue_client.account_id is None:
            msg = "`account_id` has not been fetched yet."
            raise RuntimeError(msg)
        return self._message_queue_client.account_id

    def get_screenshot(self) -> bytes:
        """Get a screenshot of the browser.

        Returns:
            bytes: Screenshot of the browser.

        Raises:
            RuntimeError: If the browser has not been launched yet.
        """
        if self._browser is None:
            msg = "Browser has not been launched yet."
            raise RuntimeError(msg)
        return self._browser.get_screenshot()

    def wait(self, timeout: float) -> PresentationBase:  # noqa: C901
        """Wait for a presentation to be detected.

        Args:
            timeout (float): Timeout in seconds.

        Returns:
            PresentationBase: Presentation detected.

        Raises:
            RuntimeError: If the browser has not been launched yet.
            RuntimeError: If the message queue client has not been launched
                yet.
            RuntimeError: If the RPA client is not running.
            PresentationTimeoutError: If the timeout has been reached.
        """
        deadline = timeout_to_deadline(timeout)

        if self._browser is None:
            msg = "Browser has not been launched yet."
            raise RuntimeError(msg)
        if self._message_queue_client is None:
            msg = "Message queue client has not been launched yet."
            raise RuntimeError(msg)

        p: PresentationBase | None = None
        while True:
            if not self.is_running():
                msg = "RPA client is not running."
                raise RuntimeError(msg)

            try:
                p = LoginPresentation(
                    self._browser,
                    self._message_queue_client,
                    self._creator,
                )
            except PresentationNotDetectedError:
                pass
            else:
                return p

            try:
                p = AuthPresentation(
                    self._browser,
                    self._message_queue_client,
                    self._creator,
                )
            except PresentationNotDetectedError:
                pass
            else:
                return p

            try:
                now = datetime.datetime.now(datetime.UTC)
                p = HomePresentation(
                    self._browser,
                    self._message_queue_client,
                    self._creator,
                    deadline - now,
                )
            except PresentationNotDetectedError:
                pass
            else:
                return p

            now = datetime.datetime.now(datetime.UTC)
            if now > deadline:
                msg = "Timeout."
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
