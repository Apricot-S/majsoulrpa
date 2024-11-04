import datetime
import email.policy
import ssl
import time
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import mktime_tz, parsedate_tz
from logging import getLogger
from typing import Any, Self

from imapclient import IMAPClient  # type: ignore[import-untyped]

from majsoulrpa.timeout import TimeoutType, to_timedelta

from ._base import (
    _YOSTAR_EMAIL_ADDRESS,
    _YOSTAR_EMAIL_SUBJECT,
    YostarLoginBase,
)

logger = getLogger(__name__)


class YostarLoginIMAP(YostarLoginBase):
    """Retrieves the verification code using IMAP."""

    def __init__(
        self,
        method: str,
        email_address: str,
        imap_server: str,
        password: str,
        mail_folder: str,
    ) -> None:
        """Initializes the instance.

        Args:
            method: The method to retrieve the verification code.
                Must be `"imap"`.
            email_address: The email address used for login.
            imap_server: The address of the IMAP server.
            password: The password for the email account.
            mail_folder: The folder in the email account.

        Raises:
            ValueError: If `method` is not `"imap"`.
        """
        if method != "imap":
            msg = f'Method "{method}" not supported. Expected "imap".'
            raise ValueError(msg)

        self._email_address = email_address
        self._imap_server = imap_server
        self._password = password
        self._mail_folder = mail_folder

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        """Creates the instance using the provided configuration.

        The following items are required in `config`:
        * config["authentication"]["method"] (str)
        * config["authentication"]["email_address"] (str)
        * config["authentication"]["imap_server"] (str)
        * config["authentication"]["password"] (str)
        * config["authentication"]["mail_folder"] (str)

        Args:
            config: A dict containing the configuration settings.

        Returns:
            An instance of `YostarLoginIMAP`.

        Raises:
            KeyError: If the required items are not found in `config`.
            TypeError: If `config` contains a invalid type value.
            ValueError: If `config["authentication"]["method"]` is not
                `"imap"`.
        """
        authentication_config = config["authentication"]
        if not isinstance(authentication_config, dict):
            msg = 'config["authentication"] must be a dict.'
            raise TypeError(msg)

        method = authentication_config["method"]
        email_address = authentication_config["email_address"]
        imap_server = authentication_config["imap_server"]
        password = authentication_config["password"]
        mail_folder = authentication_config["mail_folder"]

        if not isinstance(method, str):
            msg = 'config["authentication"]["method"] must be a str.'
            raise TypeError(msg)
        if not isinstance(email_address, str):
            msg = 'config["authentication"]["email_address"] must be a str.'
            raise TypeError(msg)
        if not isinstance(imap_server, str):
            msg = 'config["authentication"]["imap_server"] must be a str.'
            raise TypeError(msg)
        if not isinstance(password, str):
            msg = 'config["authentication"]["password"] must be a str.'
            raise TypeError(msg)
        if not isinstance(mail_folder, str):
            msg = 'config["authentication"]["mail_folder"] must be a str.'
            raise TypeError(msg)

        return cls(method, email_address, imap_server, password, mail_folder)

    def get_email_address(self) -> str:
        """Returns the email address used for login.

        Returns:
            The email address used for login.
        """
        return self._email_address

    def _get_verification_code(
        self,
        server: IMAPClient,
        start_time: datetime.datetime,
    ) -> str | None:
        now = datetime.datetime.now(tz=datetime.UTC)
        today = now.date()

        server.select_folder(self._mail_folder)
        messages_ids = server.search(
            [
                "TO",
                self._email_address,
                "FROM",
                _YOSTAR_EMAIL_ADDRESS,
                "SINCE",
                today,
            ],  # type: ignore[arg-type]
        )

        response = server.fetch(messages_ids, ["RFC822"])
        parser = BytesParser(policy=email.policy.default)

        target_date = None
        target_content = None

        for uid, msg_data in response.items():
            msg = parser.parsebytes(msg_data[b"RFC822"])  # type: ignore[arg-type]

            if not isinstance(msg, EmailMessage):
                continue

            if msg.get("Subject") != _YOSTAR_EMAIL_SUBJECT:
                # Ignore emails whose `Subject` is not
                # `Eメールアドレスの確認` as they may be
                # related to matters other than login.
                continue

            mail_date = msg.get("Date")
            if mail_date is None:
                continue
            date = datetime.datetime.fromtimestamp(
                mktime_tz(parsedate_tz(mail_date)),  # type: ignore[arg-type]
                datetime.UTC,
            )

            if date < (now - datetime.timedelta(minutes=30)):
                # The verification code is valid for 30 minutes,
                # so delete emails sent more than 30 minutes ago.
                server.delete_messages(uid)
                logger.info(
                    "Deleted mail sent more than 30 minutes ago: uid %d",
                    uid,
                )
                continue

            if date < start_time:
                # Delete emails sent before starting login.
                server.delete_messages(uid)
                logger.info(
                    "Deleted mail sent before starting login: uid %d",
                    uid,
                )
                continue

            if target_date is not None and date < target_date:
                # If another login email already exists,
                # delete the old one.
                server.delete_messages(uid)
                logger.info("Deleted mail the old one: uid %d", uid)
                continue

            target_date = date
            target_content = msg.get_content()

            server.delete_messages(uid)
            logger.info("Deleted used mail: uid %d", uid)

        if target_content is None:
            return None

        return self._extract_auth_code_from_content(target_content)

    def get_verification_code(
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

        Raises:
            ValueError: If `timeout` is greater than 1800 seconds
                (verification code expiration).
            RuntimeError: If the verification code cannot be obtained
                before the timeout period expires.
        """
        timeout = to_timedelta(timeout)

        if timeout > datetime.timedelta(seconds=1800):
            msg = (
                "Timeout is longer than verification code expiration. "
                "Set the timeout to 1800 seconds or less."
            )
            raise ValueError(msg)

        context = ssl.create_default_context()
        with IMAPClient(self._imap_server, ssl_context=context) as server:
            server.login(self._email_address, self._password)
            logger.info("Login to the mail server was successful.")

            while True:
                verification_code = self._get_verification_code(
                    server,
                    start_time,
                )
                if verification_code is not None:
                    break

                now = datetime.datetime.now(tz=datetime.UTC)
                if now > (start_time + timeout):
                    msg = "Verification code extraction timed out."
                    raise RuntimeError(msg)

                time.sleep(1.0)

        return verification_code
