import datetime
import re
from abc import ABCMeta, abstractmethod
from logging import getLogger
from typing import Any, Final

from majsoulrpa.common import TimeoutType

logger = getLogger(__name__)

YOSTAR_EMAIL_ADDRESS: Final[str] = "info@passport.yostar.co.jp"
YOSTAR_EMAIL_SUBJECT: Final[str] = "Eメールアドレスの確認"


class YostarLoginBase(metaclass=ABCMeta):
    """Provides common functionality for Yostar account logins."""

    @abstractmethod
    def __init__(self, config: dict[str, Any]) -> None:
        """Creates an instance of `YostarLoginBase`.

        Creates an instance of `YostarLoginBase` using the provided
        configuration. Subclasses can extract the necessary information
        from the `config` dictionary.

        Args:
            config: A configuration.
        """

    @abstractmethod
    def get_email_address(self) -> str:
        """Returns the email address used for login.

        Returns:
            The email address used for login.
        """

    # The verification code is a 6-digit number
    # sandwiched between HTML tags,
    # so it can search for the verification code
    # using the following regular expression.
    _PATTERN: Final = re.compile(r">(\d{6})<")

    def _extract_auth_code_from_content(self, content: str) -> str | None:
        auth_code = YostarLoginBase._PATTERN.search(content)
        if auth_code is None:
            return None
        logger.debug(
            "The auth code was successfully obtained.: %s",
            auth_code.group(1),
        )
        return auth_code.group(1)

    @abstractmethod
    def get_auth_code(
        self,
        *,
        start_time: datetime.datetime,
        timeout: TimeoutType = 1800,
    ) -> str:
        """Retrieves the verification code.

        Args:
            start_time: The time when the login process started.
            timeout: The maximum duration, in seconds, to wait for the
                verification code to be obtained. Defaults to `1800`.

        Returns:
            The obtained verification code.
        """
