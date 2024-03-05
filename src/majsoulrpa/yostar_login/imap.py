import datetime
import email.policy
import ssl
import time
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import mktime_tz, parsedate_tz
from logging import getLogger
from typing import Any

from imapclient import IMAPClient  # type: ignore[import-untyped]

from majsoulrpa.common import TimeoutType, to_timedelta

from .base import YOSTAR_EMAIL_ADDRESS, YOSTAR_EMAIL_SUBJECT, YostarLoginBase

logger = getLogger(__name__)


class YostarLoginIMAP(YostarLoginBase):
    """Retrieves the verification code using IMAP."""

    def __init__(self, config: dict[str, Any]) -> None:
        authentication_config = config["authentication"]
        self._email_address = authentication_config["email_address"]
        self._imap_server = authentication_config["imap_server"]
        self._password = authentication_config["password"]
        self._mail_folder = authentication_config["mail_folder"]

    def get_email_address(self) -> str:
        return self._email_address

    def _get_auth_code(self, *, start_time: datetime.datetime) -> str | None:
        context = ssl.create_default_context()
        with IMAPClient(self._imap_server, ssl_context=context) as server:
            server.login(self._email_address, self._password)
            logger.info("Login to the mail server was successful.")

            now = datetime.datetime.now(tz=datetime.UTC)
            today = now.date()

            server.select_folder(self._mail_folder)
            messages_ids = server.search(
                [
                    "TO",
                    self._email_address,
                    "FROM",
                    YOSTAR_EMAIL_ADDRESS,
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

                if msg.get("Subject") != YOSTAR_EMAIL_SUBJECT:
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

    def get_auth_code(
        self,
        *,
        start_time: datetime.datetime,
        timeout: TimeoutType = 1800,
    ) -> str:
        timeout = to_timedelta(timeout)

        if timeout > datetime.timedelta(seconds=1800):
            msg = (
                "Timeout is longer than verification code expiration. "
                "Set the timeout to 30 minutes or less."
            )
            raise ValueError(msg)

        while True:
            auth_code = self._get_auth_code(start_time=start_time)
            if auth_code is not None:
                break

            now = datetime.datetime.now(tz=datetime.UTC)
            if now > (start_time + timeout):
                msg = "Verification code extraction timed out."
                raise RuntimeError(msg)

            time.sleep(1.0)

        return auth_code
