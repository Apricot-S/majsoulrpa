from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage
from io import BytesIO
from typing import TYPE_CHECKING, Any, cast

import pytest

import majsoulrpa.yostar_email.s3 as s3_module
from majsoulrpa.yostar_email.s3 import (
    S3VerificationCodeProvider,
    VerificationEmailNotFoundError,
)

if TYPE_CHECKING:
    from types_boto3_s3.client import S3Client

    from majsoulrpa.yostar_email import VerificationCodeProvider

NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _accepts_code_provider(_provider: VerificationCodeProvider) -> None:
    pass


def _message(
    *,
    sender: str = "info@passport.yostar.co.jp",
    recipient: str = "user@example.com",
    subject: str = "【Yostar】メールアドレスの認証コードは　012345",
) -> bytes:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content("Synthetic test message.")
    return message.as_bytes()


class S3ClientFake:
    def __init__(
        self, objects: list[dict[str, Any]], bodies: dict[str, bytes]
    ) -> None:
        self.objects = objects
        self.bodies = bodies
        self.list_calls: list[dict[str, str]] = []
        self.get_calls: list[dict[str, str]] = []
        self.delete_calls: list[dict[str, str]] = []

    def list_objects_v2(self, **kwargs: str) -> dict[str, Any]:
        self.list_calls.append(kwargs)
        return {"Contents": self.objects, "IsTruncated": False}

    def get_object(self, **kwargs: str) -> dict[str, BytesIO]:
        self.get_calls.append(kwargs)
        return {"Body": BytesIO(self.bodies[kwargs["Key"]])}

    def delete_object(self, **kwargs: str) -> None:
        self.delete_calls.append(kwargs)


class DelayedS3ClientFake(S3ClientFake):
    def __init__(
        self,
        objects: list[dict[str, Any]],
        bodies: dict[str, bytes],
    ) -> None:
        super().__init__(objects, bodies)
        self.attempts = 0

    def list_objects_v2(self, **kwargs: str) -> dict[str, Any]:
        self.attempts += 1
        if self.attempts == 1:
            self.list_calls.append(kwargs)
            return {"Contents": [], "IsTruncated": False}
        return super().list_objects_v2(**kwargs)


def test_fetches_latest_valid_email_below_prefix() -> None:
    client = S3ClientFake(
        [
            {
                "Key": "mail/invalid",
                "LastModified": NOW - timedelta(minutes=1),
            },
            {"Key": "mail/valid", "LastModified": NOW - timedelta(minutes=2)},
            {"Key": "mail/expired", "LastModified": NOW - timedelta(hours=1)},
        ],
        {
            "mail/invalid": _message(sender="attacker@example.com"),
            "mail/valid": _message(),
        },
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        key_prefix="mail/",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )
    _accepts_code_provider(provider)

    assert asyncio.run(provider.fetch_nowait()) == "012345"
    assert client.list_calls == [
        {"Bucket": "example-bucket", "Prefix": "mail/"},
    ]
    assert [call["Key"] for call in client.get_calls] == [
        "mail/invalid",
        "mail/valid",
    ]
    assert client.delete_calls == []
    assert "user@example.com" not in repr(provider)


def test_fetch_deletes_read_matching_emails_when_requested() -> None:
    client = S3ClientFake(
        [
            {"Key": "mail/valid", "LastModified": NOW},
            {
                "Key": "mail/older",
                "LastModified": NOW - timedelta(minutes=5),
            },
            {
                "Key": "mail/expired",
                "LastModified": NOW - timedelta(hours=1),
            },
            {
                "Key": "mail/other-recipient",
                "LastModified": NOW - timedelta(minutes=1),
            },
            {
                "Key": "mail/other-subject",
                "LastModified": NOW - timedelta(minutes=2),
            },
        ],
        {
            "mail/valid": _message(),
            "mail/older": _message(sender="attacker@example.com"),
            "mail/expired": _message(),
            "mail/other-recipient": _message(recipient="other@example.com"),
            "mail/other-subject": _message(subject="Synthetic subject"),
        },
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert (
        asyncio.run(provider.fetch_nowait(delete_read_emails=True)) == "012345"
    )
    assert client.delete_calls == [
        {"Bucket": "example-bucket", "Key": "mail/valid"},
        {"Bucket": "example-bucket", "Key": "mail/older"},
        {"Bucket": "example-bucket", "Key": "mail/expired"},
    ]


def test_fetch_fails_when_no_valid_email_exists() -> None:
    client = S3ClientFake([], {})
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(VerificationEmailNotFoundError):
        asyncio.run(provider.fetch_nowait())


def test_fetch_retries_until_email_is_available() -> None:
    client = DelayedS3ClientFake(
        [
            {"Key": "mail/valid", "LastModified": NOW},
        ],
        {"mail/valid": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert (
        asyncio.run(
            provider.fetch(
                poll_interval=0.001,
                delete_read_emails=True,
            )
        )
        == "012345"
    )
    assert client.attempts == 2
    assert client.delete_calls == [
        {"Bucket": "example-bucket", "Key": "mail/valid"},
    ]


def test_fetch_creates_s3_client_once_before_polling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = DelayedS3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    created_profiles: list[str | None] = []

    def create_client(aws_profile: str | None) -> S3Client:
        created_profiles.append(aws_profile)
        return cast("S3Client", client)

    monkeypatch.setattr(s3_module, "_create_s3_client", create_client)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        aws_profile="example-profile",
        clock=lambda: NOW,
    )

    assert asyncio.run(provider.fetch(poll_interval=0.001)) == "012345"
    assert client.attempts == 2
    assert created_profiles == ["example-profile"]


def test_fetch_rejects_nonpositive_poll_interval() -> None:
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", S3ClientFake([], {})),
        clock=lambda: NOW,
    )

    with pytest.raises(ValueError, match="poll_interval"):
        asyncio.run(provider.fetch(poll_interval=0.0))


def test_missing_boto3_names_required_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_import(_name: str) -> None:
        raise ModuleNotFoundError

    monkeypatch.setattr(s3_module.importlib, "import_module", missing_import)

    with pytest.raises(ModuleNotFoundError, match="'s3' optional dependency"):
        s3_module._create_s3_client(None)
