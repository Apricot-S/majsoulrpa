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


def _message(*, sender: str = "info@passport.yostar.co.jp") -> bytes:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = "user@example.com"
    message["Subject"] = "【Yostar】メールアドレスの認証コードは　012345"
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

    def list_objects_v2(self, **kwargs: str) -> dict[str, Any]:
        self.list_calls.append(kwargs)
        return {"Contents": self.objects, "IsTruncated": False}

    def get_object(self, **kwargs: str) -> dict[str, BytesIO]:
        self.get_calls.append(kwargs)
        return {"Body": BytesIO(self.bodies[kwargs["Key"]])}


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
    provider: VerificationCodeProvider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        key_prefix="mail/",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert asyncio.run(provider.fetch()) == "012345"
    assert client.list_calls == [
        {"Bucket": "example-bucket", "Prefix": "mail/"},
    ]
    assert [call["Key"] for call in client.get_calls] == [
        "mail/invalid",
        "mail/valid",
    ]
    assert "user@example.com" not in repr(provider)


def test_fetch_fails_when_no_valid_email_exists() -> None:
    client = S3ClientFake([], {})
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(VerificationEmailNotFoundError):
        asyncio.run(provider.fetch())


def test_missing_boto3_names_required_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_import(_name: str) -> None:
        raise ModuleNotFoundError

    monkeypatch.setattr(s3_module.importlib, "import_module", missing_import)

    with pytest.raises(ModuleNotFoundError, match="'s3' optional dependency"):
        s3_module._create_s3_client(None)
