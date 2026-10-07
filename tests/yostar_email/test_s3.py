from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage
from io import BytesIO
from typing import TYPE_CHECKING, Any, cast

import pytest

import majsoulrpa.yostar_email.s3 as s3_module
from majsoulrpa.yostar_email import (
    InvalidYostarVerificationEmailError,
    YostarVerificationEmailError,
)
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


@pytest.mark.parametrize(
    "tokens",
    [
        pytest.param([None], id="missing-token"),
        pytest.param([123], id="non-string-token"),
        pytest.param([""], id="empty-token"),
        pytest.param(["synthetic-a", "synthetic-a"], id="repeated-token"),
        pytest.param(
            ["synthetic-a", "synthetic-b", "synthetic-a"], id="token-cycle"
        ),
    ],
)
def test_fetch_rejects_invalid_listing_continuation(
    tokens: list[str | int | None],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake([], {})
    responses = iter(tokens)

    def list_objects(**kwargs: str) -> dict[str, Any]:
        client.list_calls.append(kwargs)
        try:
            token = next(responses)
        except StopIteration:
            pytest.fail("Invalid continuation triggered another listing.")
        return {
            "Contents": [],
            "IsTruncated": True,
            "NextContinuationToken": token,
        }

    monkeypatch.setattr(client, "list_objects_v2", list_objects)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(ValueError, match="continuation token"):
        asyncio.run(provider.fetch_nowait())

    assert len(client.list_calls) == len(tokens)
    assert client.get_calls == []
    assert client.delete_calls == []


def test_fetch_selects_latest_email_across_listing_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake(
        [],
        {
            "mail/older": _message(),
            "mail/newer": _message(
                subject="【Yostar】メールアドレスの認証コードは　654321"
            ),
        },
    )
    pages = iter(
        [
            {
                "Contents": [
                    {
                        "Key": "mail/older",
                        "LastModified": NOW - timedelta(minutes=1),
                    }
                ],
                "IsTruncated": True,
                "NextContinuationToken": "synthetic-next",
            },
            {
                "Contents": [{"Key": "mail/newer", "LastModified": NOW}],
                "IsTruncated": False,
            },
        ]
    )

    def list_objects(**kwargs: str) -> dict[str, Any]:
        client.list_calls.append(kwargs)
        return next(pages)

    monkeypatch.setattr(client, "list_objects_v2", list_objects)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        key_prefix="mail/",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert asyncio.run(provider.fetch_nowait()) == "654321"
    assert client.list_calls == [
        {"Bucket": "example-bucket", "Prefix": "mail/"},
        {
            "Bucket": "example-bucket",
            "Prefix": "mail/",
            "ContinuationToken": "synthetic-next",
        },
    ]


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


@pytest.mark.parametrize(
    "read_failure",
    [
        pytest.param(None, id="read-success"),
        pytest.param(
            RuntimeError("Synthetic read failure"), id="read-failure"
        ),
    ],
)
def test_fetch_closes_response_body_after_read(
    read_failure: RuntimeError | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = BytesIO(_message())
    client = S3ClientFake([{"Key": "mail/valid", "LastModified": NOW}], {})

    def get_object(**kwargs: str) -> dict[str, BytesIO]:
        client.get_calls.append(kwargs)
        return {"Body": body}

    monkeypatch.setattr(client, "get_object", get_object)
    if read_failure is not None:

        def fail_read(_size: int = -1) -> bytes:
            raise read_failure

        monkeypatch.setattr(body, "read", fail_read)

    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )
    if read_failure is None:
        assert asyncio.run(provider.fetch_nowait()) == "012345"
    else:
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(provider.fetch_nowait())
        assert exc_info.value is read_failure

    assert body.closed
    assert len(client.get_calls) == 1
    assert client.delete_calls == []


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
        key_prefix="example-prefix/",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(VerificationEmailNotFoundError) as exc_info:
        asyncio.run(provider.fetch_nowait())

    assert isinstance(exc_info.value, YostarVerificationEmailError)
    assert not isinstance(exc_info.value, InvalidYostarVerificationEmailError)
    for error in (str(exc_info.value), repr(exc_info.value)):
        assert "user@example.com" not in error
        assert "example-bucket" not in error
        assert "example-prefix/" not in error
    assert len(client.list_calls) == 1


@pytest.mark.parametrize(
    "failure",
    [
        pytest.param(YostarVerificationEmailError(), id="base-email-error"),
        pytest.param(
            InvalidYostarVerificationEmailError(), id="invalid-email-error"
        ),
        pytest.param(RuntimeError(), id="external-operation-error"),
        pytest.param(asyncio.CancelledError(), id="cancellation"),
    ],
)
def test_fetch_propagates_non_missing_failure_without_retry(
    failure: BaseException,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake([], {})
    attempts = 0

    def fail_listing(**_kwargs: str) -> dict[str, Any]:
        nonlocal attempts
        attempts += 1
        raise failure

    async def unexpected_sleep(_delay: float) -> None:
        pytest.fail("Only missing email may trigger polling sleep.")

    monkeypatch.setattr(client, "list_objects_v2", fail_listing)
    monkeypatch.setattr(s3_module.asyncio, "sleep", unexpected_sleep)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(type(failure)) as exc_info:
        asyncio.run(provider.fetch())

    assert exc_info.value is failure
    assert attempts == 1
    assert client.get_calls == []
    assert client.delete_calls == []


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
        poll_interval=0.001,
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert (
        asyncio.run(
            provider.fetch(
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
        poll_interval=0.001,
        clock=lambda: NOW,
    )

    assert asyncio.run(provider.fetch()) == "012345"
    assert client.attempts == 2
    assert created_profiles == ["example-profile"]


@pytest.mark.parametrize(
    "poll_interval",
    [
        pytest.param(0.0, id="zero"),
        pytest.param(-1.0, id="negative"),
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
        pytest.param(1800.0, id="at-expiration"),
        pytest.param(1800.001, id="above-expiration"),
    ],
)
def test_provider_rejects_invalid_poll_interval(poll_interval: float) -> None:
    with pytest.raises(ValueError, match="poll_interval"):
        S3VerificationCodeProvider(
            email_address="user@example.com",
            bucket_name="example-bucket",
            poll_interval=poll_interval,
            client=cast("S3Client", S3ClientFake([], {})),
            clock=lambda: NOW,
        )


def test_provider_accepts_poll_interval_just_below_expiration() -> None:
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        poll_interval=1799.999,
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert asyncio.run(provider.fetch_nowait()) == "012345"


def test_missing_boto3_names_required_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failure = ModuleNotFoundError("Synthetic missing dependency", name="boto3")

    def missing_import(_name: str) -> None:
        raise failure

    monkeypatch.setattr(s3_module.importlib, "import_module", missing_import)

    with pytest.raises(
        ModuleNotFoundError, match="'s3' optional dependency"
    ) as exc_info:
        s3_module._create_s3_client(None)

    assert exc_info.value.__cause__ is failure


@pytest.mark.parametrize(
    "missing_name",
    [
        pytest.param("botocore", id="transitive-dependency"),
        pytest.param(None, id="unknown-missing-module"),
    ],
)
def test_boto3_import_preserves_unrelated_module_failure(
    missing_name: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failure = ModuleNotFoundError(
        "Synthetic dependency failure", name=missing_name
    )

    def fail_import(_name: str) -> None:
        raise failure

    monkeypatch.setattr(s3_module.importlib, "import_module", fail_import)

    with pytest.raises(ModuleNotFoundError) as exc_info:
        s3_module._create_s3_client(None)

    assert exc_info.value is failure
