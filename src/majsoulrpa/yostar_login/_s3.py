import datetime
import email.policy
import time
from email.message import EmailMessage
from email.parser import BytesParser
from logging import getLogger
from typing import Any, Self

import boto3

from majsoulrpa.timeout import TimeoutType, to_timedelta

from ._base import (
    _YOSTAR_EMAIL_ADDRESS,
    _YOSTAR_EMAIL_SUBJECT,
    YostarLoginBase,
)

logger = getLogger(__name__)


class YostarLoginS3(YostarLoginBase):
    """Retrieves the verification code using an S3 bucket."""

    def __init__(
        self,
        method: str,
        email_address: str,
        bucket_name: str,
        key_prefix: str,
        aws_profile: str | None = None,
    ) -> None:
        """Initializes the instance.

        Args:
            method: The method to retrieve the verification code.
                Must be `"s3"`.
            email_address: The email address used for login.
            bucket_name: The name of the S3 bucket where emails are
                stored.
            key_prefix: The prefix to filter objects within the S3
                bucket.
            aws_profile: The AWS CLI profile to use for authentication.
                If not given, then the default profile is used.
                Defaults to `None`.

        Raises:
            ValueError: If `method` is not `"s3"`.
        """
        if method != "s3":
            msg = f'Method "{method}" not supported. Expected "s3".'
            raise ValueError(msg)

        self._email_address = email_address
        if aws_profile is None:
            s3_client = boto3.resource("s3")
        else:
            session = boto3.Session(profile_name=aws_profile)
            s3_client = session.resource("s3")
        self._s3_bucket = s3_client.Bucket(bucket_name)
        self._key_prefix = key_prefix

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        """Creates the instance using the provided configuration.

        The following items are required in `config`:

        * config["authentication"]["method"] (str)
        * config["authentication"]["email_address"] (str)
        * config["authentication"]["bucket_name"] (str)
        * config["authentication"]["key_prefix"] (str)

        The following items can be set as options:

        * config["authentication"]["aws_profile"] (str)

        Args:
            config: A dict containing the configuration settings.

        Returns:
            An instance of `YostarLoginS3`.

        Raises:
            KeyError: If the required items are not found in `config`.
            TypeError: If `config` contains a invalid type value.
            ValueError: If `config["authentication"]["method"]` is not
                `"s3"`.
        """
        authentication_config: dict[str, Any] = config["authentication"]
        if not isinstance(authentication_config, dict):
            msg = 'config["authentication"] must be a dict.'
            raise TypeError(msg)

        method = authentication_config["method"]
        email_address = authentication_config["email_address"]
        bucket_name = authentication_config["bucket_name"]
        key_prefix = authentication_config["key_prefix"]
        aws_profile = authentication_config.get("aws_profile")

        if not isinstance(method, str):
            msg = 'config["authentication"]["method"] must be a str.'
            raise TypeError(msg)
        if not isinstance(email_address, str):
            msg = 'config["authentication"]["email_address"] must be a str.'
            raise TypeError(msg)
        if not isinstance(bucket_name, str):
            msg = 'config["authentication"]["bucket_name"] must be a str.'
            raise TypeError(msg)
        if not isinstance(key_prefix, str):
            msg = 'config["authentication"]["key_prefix"] must be a str.'
            raise TypeError(msg)
        if aws_profile is not None and not isinstance(aws_profile, str):
            msg = 'config["authentication"]["aws_profile"] must be a str.'
            raise TypeError(msg)

        return cls(method, email_address, bucket_name, key_prefix, aws_profile)

    def get_email_address(self) -> str:
        """Returns the email address used for login.

        Returns:
            The email address used for login.
        """
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

    def _get_verification_code(
        self,
        start_time: datetime.datetime,
    ) -> str | None:
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
            if mail.get("From") != _YOSTAR_EMAIL_ADDRESS:
                # Ignore emails whose `From` is not
                # `info@passport.yostar.co.jp`
                # as they may be related to matters other than login.
                continue

            if "Subject" not in mail:
                continue
            if mail.get("Subject") != _YOSTAR_EMAIL_SUBJECT:
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

        while True:
            verification_code = self._get_verification_code(start_time)
            if verification_code is not None:
                break

            now = datetime.datetime.now(tz=datetime.UTC)
            if now > (start_time + timeout):
                msg = "Verification code extraction timed out."
                raise RuntimeError(msg)

            time.sleep(1.0)

        return verification_code
