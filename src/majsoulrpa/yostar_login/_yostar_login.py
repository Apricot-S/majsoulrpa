import datetime
import email.policy
import re
import ssl
import time
from abc import ABCMeta, abstractmethod
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import mktime_tz, parsedate_tz
from logging import getLogger
from typing import Any, Final

import boto3
from imapclient import IMAPClient  # type: ignore[import-untyped]

from majsoulrpa.common import TimeoutType, to_timedelta

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
        """Retrieves the authentication code.

        Args:
            start_time: The time when the login process started.
            timeout: The maximum duration, in seconds, to wait for the
                authentication code to be obtained. Defaults to `1800`.

        Returns:
            The obtained authentication code.
        """


class YostarLoginIMAP(YostarLoginBase):
    """Retrieves the authentication code using IMAP."""

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


class YostarLoginS3(YostarLoginBase):
    """Retrieves the authentication code using an S3 bucket."""

    def __init__(self, config: dict[str, Any]) -> None:
        authentication_config = config["authentication"]
        method = authentication_config["method"]
        if method != "s3":
            msg = f"{method}: Authentication method not implemented."
            raise NotImplementedError(msg)

        self._email_address = authentication_config["email_address"]
        if "aws_profile" not in authentication_config:
            s3_client = boto3.resource("s3")
        else:
            aws_profile = authentication_config["aws_profile"]
            session = boto3.Session(profile_name=aws_profile)
            s3_client = session.resource("s3")
        bucket_name = authentication_config["bucket_name"]
        self._s3_bucket = s3_client.Bucket(bucket_name)
        self._key_prefix = authentication_config["key_prefix"]

    def get_email_address(self) -> str:
        return self._email_address

    def _get_authentication_emails(self) -> dict[str, EmailMessage]:
        objects = self._s3_bucket.objects.filter(Prefix=self._key_prefix)

        emails: dict[str, EmailMessage] = {}
        email_parser = BytesParser(policy=email.policy.default)

        for summary in objects:
            key = summary.key
            obj = summary.get()
            body = obj["Body"]
            obj_bytes = body.read()
            message = email_parser.parsebytes(obj_bytes)
            assert isinstance(message, EmailMessage)  # noqa: S101
            emails[key] = message

        return emails

    def _get_auth_code(self, *, start_time: datetime.datetime) -> str | None:  # noqa: C901
        emails = self._get_authentication_emails()

        target_date = None
        target_content = None

        def delete_object(key: str) -> None:
            self._s3_bucket.delete_objects(Delete={"Objects": [{"Key": key}]})

        for key, mail in emails.items():
            if "Date" not in mail:
                delete_object(key)
                logger.info("Deleted the S3 object `%s`.", key)
                continue

            date = datetime.datetime.strptime(
                mail["Date"],
                "%a, %d %b %Y %H:%M:%S %z",
            )

            if "To" not in mail:
                delete_object(key)
                logger.info("Deleted the S3 object `%s`.", key)
                continue
            if mail.get("To") != self._email_address:
                # E-mails with different destinations may be sent
                # to other crawlers, so ignore them.
                continue

            if "From" not in mail:
                delete_object(key)
                logger.info("Deleted the S3 object `%s`.", key)
                continue
            if mail.get("From") != YOSTAR_EMAIL_ADDRESS:
                # Ignore emails whose `From` is not
                # `info@passport.yostar.co.jp`
                # as they may be related to matters other than login.
                continue

            if "Subject" not in mail:
                continue
            if mail.get("Subject") != YOSTAR_EMAIL_SUBJECT:
                # Ignore emails whose `Subject` is not
                # `Eメールアドレスの確認`
                # as they may be related to matters other than login.
                continue

            now = datetime.datetime.now(tz=datetime.UTC)

            if date < (now - datetime.timedelta(minutes=30)):
                # The verification code is valid for 30 minutes,
                # so delete emails sent more than 30 minutes ago.
                delete_object(key)
                logger.info("Deleted the S3 object `%s`.", key)
                continue

            if date < start_time:
                # Delete emails sent before starting login.
                delete_object(key)
                logger.info("Deleted the S3 object `%s`.", key)
                continue

            if target_date is not None and date < target_date:
                # If another login email already exists,
                # delete the old one.
                delete_object(key)
                logger.info("Deleted the S3 object `%s`.", key)
                continue

            target_date = date
            target_content = mail.get_content()

            delete_object(key)
            logger.info("Deleted the S3 object `%s`.", key)

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
