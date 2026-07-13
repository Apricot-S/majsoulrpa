from __future__ import annotations

import asyncio
import importlib
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from majsoulrpa.yostar_email.email import extract_verification_code
from majsoulrpa.yostar_email.errors import (
    InvalidYostarVerificationEmailError,
    YostarVerificationEmailError,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from types_boto3_s3.client import S3Client


class VerificationEmailNotFoundError(YostarVerificationEmailError):
    """No current valid verification email was found."""


class S3VerificationCodeProvider:
    """Fetch Yostar verification emails stored as S3 objects."""

    def __init__(
        self,
        *,
        email_address: str,
        bucket_name: str,
        key_prefix: str = "",
        aws_profile: str | None = None,
        client: S3Client | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._email_address = email_address
        self._bucket_name = bucket_name
        self._key_prefix = key_prefix
        self._aws_profile = aws_profile
        self._client = client
        self._clock = clock or _utc_now

    async def fetch(self) -> str:
        """Return the code from the newest current matching S3 email."""
        return await asyncio.to_thread(self._fetch)

    def _fetch(self) -> str:
        client = self._client or _create_s3_client(self._aws_profile)
        now = self._clock()
        objects = _list_objects(
            client,
            self._bucket_name,
            self._key_prefix,
        )
        candidates = sorted(
            objects,
            key=lambda item: item["LastModified"],
            reverse=True,
        )
        for item in candidates:
            received_at = item.get("LastModified")
            key = item.get("Key")
            if not isinstance(received_at, datetime) or not isinstance(
                key,
                str,
            ):
                continue
            if received_at.tzinfo is None:
                continue
            age = now - received_at
            if age < timedelta(0) or age >= timedelta(minutes=30):
                continue
            response = client.get_object(Bucket=self._bucket_name, Key=key)
            body = response["Body"].read()
            if not isinstance(body, bytes):
                msg = "S3 verification email body is not bytes."
                raise TypeError(msg)
            try:
                return extract_verification_code(
                    body,
                    recipient=self._email_address,
                    received_at=received_at,
                    now=now,
                )
            except InvalidYostarVerificationEmailError:
                continue
        msg = "No current Yostar verification email was found in S3."
        raise VerificationEmailNotFoundError(msg)


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _list_objects(
    client: S3Client,
    bucket_name: str,
    key_prefix: str,
) -> list[Any]:
    objects: list[Any] = []
    continuation_token: str | None = None
    while True:
        if continuation_token is None:
            response = client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=key_prefix,
            )
        else:
            response = client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=key_prefix,
                ContinuationToken=continuation_token,
            )
        objects.extend(response.get("Contents", []))
        if not response.get("IsTruncated", False):
            return objects
        continuation_token = response.get("NextContinuationToken")
        if not isinstance(continuation_token, str):
            msg = "S3 listing is truncated without a continuation token."
            raise TypeError(msg)


def _create_s3_client(aws_profile: str | None) -> S3Client:
    try:
        boto3 = importlib.import_module("boto3")
    except ModuleNotFoundError as error:
        msg = (
            "S3VerificationCodeProvider requires the 's3' optional "
            "dependency. Install it with: pip install 'majsoulrpa[s3]'"
        )
        raise ModuleNotFoundError(msg) from error
    session = boto3.Session(profile_name=aws_profile)
    return session.client("s3")


__all__ = ["S3VerificationCodeProvider", "VerificationEmailNotFoundError"]
