from __future__ import annotations

import asyncio
import importlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from majsoulrpa.yostar_email.constants import VERIFICATION_EMAIL_EXPIRATION
from majsoulrpa.yostar_email.email import VerificationEmail
from majsoulrpa.yostar_email.errors import (
    InvalidYostarVerificationEmailError,
    YostarVerificationEmailError,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from types_boto3_s3.client import S3Client


class VerificationEmailNotFoundError(YostarVerificationEmailError):
    """No current valid verification email was found."""


@dataclass(frozen=True, slots=True)
class _S3EmailCandidate:
    key: str
    received_at: datetime


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

    async def fetch(
        self,
        *,
        poll_interval: float = 5.0,
        delete_read_emails: bool = False,
    ) -> str:
        """Poll S3 and optionally delete matching emails read."""
        if poll_interval <= 0.0:
            msg = "poll_interval must be greater than zero."
            raise ValueError(msg)

        client = await self._resolve_client()
        while True:
            try:
                return await self._run_fetch_once(
                    client,
                    delete_read_emails=delete_read_emails,
                )
            except VerificationEmailNotFoundError:
                await asyncio.sleep(poll_interval)

    async def fetch_nowait(self, *, delete_read_emails: bool = False) -> str:
        """Check S3 once and optionally delete matching emails read."""
        client = await self._resolve_client()
        return await self._run_fetch_once(
            client,
            delete_read_emails=delete_read_emails,
        )

    async def _resolve_client(self) -> S3Client:
        if self._client is not None:
            return self._client
        return await asyncio.to_thread(_create_s3_client, self._aws_profile)

    async def _run_fetch_once(
        self,
        client: S3Client,
        *,
        delete_read_emails: bool,
    ) -> str:
        return await asyncio.to_thread(
            self._fetch_once,
            client,
            delete_read_emails=delete_read_emails,
        )

    def _fetch_once(
        self,
        client: S3Client,
        *,
        delete_read_emails: bool,
    ) -> str:
        now = self._clock()
        candidates = _list_email_candidates(
            client,
            bucket_name=self._bucket_name,
            key_prefix=self._key_prefix,
        )
        verification_code: str | None = None
        keys_to_delete: list[str] = []
        for candidate in candidates:
            is_current = _is_current(candidate.received_at, now=now)
            if not delete_read_emails and not is_current:
                continue

            email = VerificationEmail.parse(
                _read_object(
                    client,
                    bucket_name=self._bucket_name,
                    key=candidate.key,
                )
            )

            if delete_read_emails and email.matches_deletion_condition(
                recipient=self._email_address,
            ):
                keys_to_delete.append(candidate.key)

            if verification_code is not None or not is_current:
                continue

            try:
                verification_code = email.extract_code(
                    recipient=self._email_address,
                )
            except InvalidYostarVerificationEmailError:
                continue

        _delete_objects(
            client,
            bucket_name=self._bucket_name,
            keys=keys_to_delete,
        )
        if verification_code is not None:
            return verification_code
        msg = "No current Yostar verification email was found in S3."
        raise VerificationEmailNotFoundError(msg)


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _list_email_candidates(
    client: S3Client,
    *,
    bucket_name: str,
    key_prefix: str,
) -> list[_S3EmailCandidate]:
    candidates: list[_S3EmailCandidate] = []
    for item in _list_objects(client, bucket_name, key_prefix):
        received_at = item.get("LastModified")
        key = item.get("Key")
        if (
            isinstance(received_at, datetime)
            and received_at.tzinfo is not None
            and isinstance(key, str)
        ):
            candidates.append(
                _S3EmailCandidate(key=key, received_at=received_at)
            )
    return sorted(
        candidates,
        key=lambda candidate: candidate.received_at,
        reverse=True,
    )


def _is_current(received_at: datetime, *, now: datetime) -> bool:
    age = now - received_at
    return timedelta(0) <= age < VERIFICATION_EMAIL_EXPIRATION


def _read_object(client: S3Client, *, bucket_name: str, key: str) -> bytes:
    response = client.get_object(Bucket=bucket_name, Key=key)
    body = response["Body"].read()
    if not isinstance(body, bytes):
        msg = "S3 verification email body is not bytes."
        raise TypeError(msg)
    return body


def _delete_objects(
    client: S3Client,
    *,
    bucket_name: str,
    keys: list[str],
) -> None:
    for key in keys:
        client.delete_object(Bucket=bucket_name, Key=key)


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
