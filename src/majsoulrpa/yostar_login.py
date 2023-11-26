import datetime
import email.policy
import re
import ssl
import time
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import mktime_tz, parsedate_tz
from logging import getLogger
from typing import Any, Final

from imapclient import IMAPClient  #type: ignore[import-untyped]

from .common import TimeoutType

logger = getLogger(__name__)

YOSTAR_EMAIL_ADDRESS: Final[str] = "info@passport.yostar.co.jp"
YOSTAR_EMAIL_SUBJECT: Final[str] = "Eメールアドレスの確認"


class YostarLogin:

    def __init__(self, config: dict[str, Any]) -> None:
        self._email_address = config["email_address"]
        self._smtp_server = config["smtp_server"]
        self._app_password = config["app_password"]
        self._mail_folder = config["mail_folder"]

    def get_email_address(self) -> str:
        return self._email_address

    def _get_auth_code(self, *, start_time: datetime.datetime) -> str | None:
        context = ssl.create_default_context()
        with IMAPClient(self._smtp_server, ssl_context=context) as server:
            server.login(self._email_address, self._app_password)
            log_msg = "Login to the mail server was successful."
            logger.info(log_msg)

            now = datetime.datetime.now(tz=datetime.UTC)
            today = now.date()

            server.select_folder(self._mail_folder)
            messages_ids = server.search([
                "TO", self._email_address,
                "FROM", YOSTAR_EMAIL_ADDRESS,
                "SINCE", today,
            ]) # type: ignore[arg-type]

            response = server.fetch(messages_ids, ["RFC822"])
            parser = BytesParser(policy=email.policy.default)

            target_date = None
            target_content = None

            for uid, msg_data in response.items():
                msg = parser.parsebytes(msg_data[b"RFC822"]) # type: ignore[arg-type]

                if not isinstance(msg, EmailMessage):
                    continue

                if msg.get("Subject") != YOSTAR_EMAIL_SUBJECT:
                    continue

                mail_date = msg.get("Date")
                if mail_date is None:
                    continue
                date = datetime.datetime.fromtimestamp(
                    mktime_tz(parsedate_tz(mail_date)), datetime.UTC,  #type: ignore[arg-type]
                )

                # The authentication code is valid for 30 minutes,
                # so delete emails sent more than 30 minutes ago.
                if date < (now - datetime.timedelta(minutes=30)):
                    server.delete_messages(uid)
                    log_msg = (
                        "Deleted mail sent more than 30 minutes ago"
                        f": uid {uid}"
                    )
                    logger.info(log_msg)
                    continue

                # Delete emails sent before starting login.
                if date < start_time:
                    server.delete_messages(uid)
                    log_msg = (
                        f"Deleted mail sent before starting login: uid {uid}"
                    )
                    logger.info(log_msg)
                    continue

                # If another login email already exists,
                # delete the old one.
                if target_date is not None and date < target_date:
                    server.delete_messages(uid)
                    log_msg = f"Deleted mail the old one: uid {uid}"
                    logger.info(log_msg)
                    continue

                target_date = date
                target_content = msg.get_content()

                server.delete_messages(uid)
                log_msg = f"Deleted used mail: uid {uid}"
                logger.info(log_msg)

            if target_content is None:
                return None

            # The authentication code is a 6-digit number
            # sandwiched between HTML tags,
            # so it can search for the authentication code
            # using the following regular expression.
            auth_code = re.search(r">(\d{6})<", target_content)
            if auth_code is None:
                return None
            log_msg = f"The auth code was successfully obtained.: {auth_code}"
            logger.debug(log_msg)

            return auth_code.group(1)

    def get_auth_code(
        self, *, start_time: datetime.datetime, timeout: TimeoutType,
    ) -> str:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        while True:
            auth_code = self._get_auth_code(start_time=start_time)
            if auth_code is not None:
                break

            now = datetime.datetime.now(tz=datetime.UTC)
            if now > (start_time + timeout):
                msg = "Extraction of the authentication has timed out."
                raise RuntimeError(msg)

            time.sleep(3.0)

        return auth_code
