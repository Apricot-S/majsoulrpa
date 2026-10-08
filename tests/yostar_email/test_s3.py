from __future__ import annotations

import asyncio
import threading
from datetime import UTC, datetime, timedelta, tzinfo
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
        self.close_calls = 0

    def close(self) -> None:
        self.close_calls += 1

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


def test_fetch_uses_injected_falsey_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FalseyClock:
        def __init__(self) -> None:
            self.calls = 0

        def __bool__(self) -> bool:
            return False

        def __call__(self) -> datetime:
            self.calls += 1
            return NOW

    def unexpected_default_clock() -> datetime:
        pytest.fail("An injected clock must not be replaced.")

    monkeypatch.setattr(s3_module, "utc_now", unexpected_default_clock)
    clock = FalseyClock()
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=clock,
    )

    assert asyncio.run(provider.fetch_nowait()) == "012345"
    assert clock.calls == 3


@pytest.mark.parametrize("method_name", ["fetch", "fetch_nowait"])
def test_fetch_uses_injected_falsey_client_without_creating_client(
    method_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FalseyS3Client(S3ClientFake):
        def __bool__(self) -> bool:
            return False

    def unexpected_creation(_aws_profile: str | None) -> S3Client:
        pytest.fail("An injected client must not be replaced.")

    monkeypatch.setattr(s3_module, "_create_s3_client", unexpected_creation)
    client = FalseyS3Client(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert asyncio.run(getattr(provider, method_name)()) == "012345"
    assert client.list_calls == [
        {"Bucket": "example-bucket", "Prefix": ""},
    ]
    assert [call["Key"] for call in client.get_calls] == ["mail/valid"]
    assert client.delete_calls == []


class UndefinedOffsetTimezone(tzinfo):
    def utcoffset(self, _dt: datetime | None) -> None:
        return None

    def dst(self, _dt: datetime | None) -> None:
        return None

    def tzname(self, _dt: datetime | None) -> None:
        return None


@pytest.mark.parametrize("timestamp_kind", ["naive", "undefined-offset"])
def test_fetch_rejects_undefined_clock_offset_before_s3_access(
    timestamp_kind: str,
) -> None:
    timestamp = NOW.replace(
        tzinfo=None if timestamp_kind == "naive" else UndefinedOffsetTimezone()
    )
    client = S3ClientFake([], {})
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: timestamp,
    )

    with pytest.raises(ValueError, match="timezone information"):
        asyncio.run(provider.fetch_nowait())

    assert client.list_calls == []
    assert client.get_calls == []
    assert client.delete_calls == []


@pytest.mark.parametrize("timestamp_kind", ["naive", "undefined-offset"])
def test_fetch_excludes_candidate_with_undefined_timestamp_offset(
    timestamp_kind: str,
) -> None:
    timestamp = NOW.replace(
        tzinfo=None if timestamp_kind == "naive" else UndefinedOffsetTimezone()
    )
    client = S3ClientFake(
        [
            {"Key": "mail/invalid-date", "LastModified": timestamp},
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
        asyncio.run(provider.fetch_nowait(delete_read_emails=True)) == "012345"
    )
    assert [call["Key"] for call in client.get_calls] == ["mail/valid"]
    assert [call["Key"] for call in client.delete_calls] == ["mail/valid"]


class RollbackTimezone(tzinfo):
    def utcoffset(self, dt: datetime | None) -> timedelta | None:
        if dt is None:
            return None
        return timedelta(hours=2 - dt.fold)

    def dst(self, _dt: datetime | None) -> timedelta:
        return timedelta(0)

    def tzname(self, _dt: datetime | None) -> str:
        return "Synthetic"


def test_fetch_excludes_expired_email_across_clock_rollback() -> None:
    zone = RollbackTimezone()
    current_time = NOW.replace(hour=2, minute=55, tzinfo=zone, fold=1)
    expired_at = NOW.replace(hour=2, minute=50, tzinfo=zone, fold=0)
    valid_at = NOW.replace(hour=2, minute=40, tzinfo=zone, fold=1)
    client = S3ClientFake(
        [
            {"Key": "mail/expired", "LastModified": expired_at},
            {"Key": "mail/valid", "LastModified": valid_at},
        ],
        {"mail/valid": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: current_time,
    )

    assert asyncio.run(provider.fetch_nowait()) == "012345"
    assert [call["Key"] for call in client.get_calls] == ["mail/valid"]


def test_fetch_selects_latest_email_by_utc_across_clock_rollback() -> None:
    zone = RollbackTimezone()
    current_time = NOW.replace(hour=2, minute=10, tzinfo=zone, fold=1)
    older_at = NOW.replace(hour=2, minute=55, tzinfo=zone, fold=0)
    newer_at = NOW.replace(hour=2, minute=5, tzinfo=zone, fold=1)
    client = S3ClientFake(
        [
            {"Key": "mail/older", "LastModified": older_at},
            {"Key": "mail/newer", "LastModified": newer_at},
        ],
        {
            "mail/older": _message(),
            "mail/newer": _message(
                subject="【Yostar】メールアドレスの認証コードは　654321"
            ),
        },
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: current_time,
    )

    assert asyncio.run(provider.fetch_nowait()) == "654321"
    assert [call["Key"] for call in client.get_calls] == ["mail/newer"]


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


def test_fetch_rejects_partial_listing_after_later_page_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake([], {"mail/valid": _message()})
    failure = RuntimeError("Synthetic second page failure")

    def list_objects(**kwargs: str) -> dict[str, Any]:
        client.list_calls.append(kwargs)
        if len(client.list_calls) == 1:
            return {
                "Contents": [{"Key": "mail/valid", "LastModified": NOW}],
                "IsTruncated": True,
                "NextContinuationToken": "synthetic-next",
            }
        raise failure

    async def unexpected_sleep(_delay: float) -> None:
        pytest.fail("Listing failure must not trigger polling retry.")

    monkeypatch.setattr(client, "list_objects_v2", list_objects)
    monkeypatch.setattr(s3_module.asyncio, "sleep", unexpected_sleep)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(provider.fetch(delete_read_emails=True))

    assert exc_info.value is failure
    assert len(client.list_calls) == 2
    assert client.list_calls[1]["ContinuationToken"] == "synthetic-next"
    assert client.get_calls == []
    assert client.delete_calls == []


@pytest.mark.parametrize("delete_read_emails", [False, True])
def test_fetch_rejects_email_expiring_during_body_read(
    *,
    delete_read_emails: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current_time = NOW
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    original_get = client.get_object

    def delayed_get(**kwargs: str) -> dict[str, BytesIO]:
        nonlocal current_time
        current_time = NOW + timedelta(minutes=30)
        return original_get(**kwargs)

    monkeypatch.setattr(client, "get_object", delayed_get)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: current_time,
    )

    with pytest.raises(VerificationEmailNotFoundError):
        asyncio.run(
            provider.fetch_nowait(delete_read_emails=delete_read_emails)
        )

    assert [call["Key"] for call in client.get_calls] == ["mail/valid"]
    assert [call["Key"] for call in client.delete_calls] == (
        ["mail/valid"] if delete_read_emails else []
    )


def test_fetch_skips_email_expiring_during_listing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current_time = NOW
    client = S3ClientFake([{"Key": "mail/expired", "LastModified": NOW}], {})
    original_list = client.list_objects_v2

    def delayed_list(**kwargs: str) -> dict[str, Any]:
        nonlocal current_time
        current_time = NOW + timedelta(minutes=30)
        return original_list(**kwargs)

    monkeypatch.setattr(client, "list_objects_v2", delayed_list)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: current_time,
    )

    with pytest.raises(VerificationEmailNotFoundError):
        asyncio.run(provider.fetch_nowait())

    assert client.get_calls == []
    assert client.delete_calls == []


def test_fetch_rejects_code_expiring_during_deletion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current_time = NOW
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    original_delete = client.delete_object

    def delayed_delete(**kwargs: str) -> None:
        nonlocal current_time
        current_time = NOW + timedelta(minutes=30)
        original_delete(**kwargs)

    monkeypatch.setattr(client, "delete_object", delayed_delete)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: current_time,
    )

    with pytest.raises(VerificationEmailNotFoundError):
        asyncio.run(provider.fetch_nowait(delete_read_emails=True))

    assert [call["Key"] for call in client.delete_calls] == ["mail/valid"]


def test_fetch_without_deletion_stops_after_valid_code() -> None:
    client = S3ClientFake(
        [
            {"Key": "mail/newest", "LastModified": NOW},
            {"Key": "mail/older", "LastModified": NOW - timedelta(minutes=1)},
        ],
        {"mail/newest": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert asyncio.run(provider.fetch_nowait()) == "012345"
    assert [call["Key"] for call in client.get_calls] == ["mail/newest"]
    assert client.delete_calls == []


@pytest.mark.parametrize("missing_field", ["Key", "LastModified"])
def test_fetch_excludes_listing_entry_with_missing_candidate_field(
    missing_field: str,
) -> None:
    incomplete: dict[str, Any] = {
        "Key": "mail/incomplete",
        "LastModified": NOW,
    }
    del incomplete[missing_field]
    client = S3ClientFake(
        [incomplete, {"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
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
    assert [call["Key"] for call in client.get_calls] == ["mail/valid"]
    assert [call["Key"] for call in client.delete_calls] == ["mail/valid"]


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
    "outside_key",
    [
        pytest.param("mail-other/message", id="similar-prefix"),
        pytest.param("other/mail/message", id="prefix-in-middle"),
    ],
)
@pytest.mark.parametrize("delete_read_emails", [False, True])
def test_fetch_excludes_keys_outside_selected_prefix(
    *,
    outside_key: str,
    delete_read_emails: bool,
) -> None:
    client = S3ClientFake(
        [
            {"Key": outside_key, "LastModified": NOW},
            {"Key": "mail/valid", "LastModified": NOW - timedelta(minutes=1)},
        ],
        {"mail/valid": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        key_prefix="mail/",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    assert (
        asyncio.run(
            provider.fetch_nowait(delete_read_emails=delete_read_emails)
        )
        == "012345"
    )
    assert [call["Key"] for call in client.get_calls] == ["mail/valid"]
    assert [call["Key"] for call in client.delete_calls] == (
        ["mail/valid"] if delete_read_emails else []
    )


@pytest.mark.parametrize(
    "read_failure",
    [
        pytest.param(None, id="read-success"),
        pytest.param(
            RuntimeError("Synthetic read failure"), id="read-failure"
        ),
    ],
)
@pytest.mark.parametrize(
    "close_failure",
    [
        pytest.param(None, id="close-success"),
        pytest.param(
            RuntimeError("Synthetic close failure"), id="close-failure"
        ),
    ],
)
def test_fetch_closes_response_body_and_preserves_failures(
    read_failure: RuntimeError | None,
    close_failure: RuntimeError | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = BytesIO(_message())
    original_close = body.close
    close_calls = 0

    def close_body() -> None:
        nonlocal close_calls
        close_calls += 1
        original_close()
        if close_failure is not None:
            raise close_failure

    monkeypatch.setattr(body, "close", close_body)
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
    expected_failure = (
        close_failure if close_failure is not None else read_failure
    )
    if expected_failure is None:
        assert asyncio.run(provider.fetch_nowait()) == "012345"
    else:
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(provider.fetch_nowait())
        assert exc_info.value is expected_failure
        if read_failure is not None and close_failure is not None:
            assert exc_info.value.__context__ is read_failure

    assert body.closed
    assert close_calls == 1
    assert len(client.get_calls) == 1
    assert client.delete_calls == []


@pytest.mark.parametrize("failure_index", [0, 1], ids=["first", "partial"])
def test_fetch_propagates_deletion_failure_without_retry(
    failure_index: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    keys = ["mail/newest", "mail/older", "mail/oldest"]
    client = S3ClientFake(
        [
            {"Key": key, "LastModified": NOW - timedelta(minutes=index)}
            for index, key in enumerate(keys)
        ],
        dict.fromkeys(keys, _message()),
    )
    failure = RuntimeError("Synthetic deletion failure")

    def delete_object(**kwargs: str) -> None:
        client.delete_calls.append(kwargs)
        if kwargs["Key"] == keys[failure_index]:
            raise failure

    async def unexpected_sleep(_delay: float) -> None:
        pytest.fail("Deletion failure must not trigger polling retry.")

    monkeypatch.setattr(client, "delete_object", delete_object)
    monkeypatch.setattr(s3_module.asyncio, "sleep", unexpected_sleep)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(provider.fetch(delete_read_emails=True))

    assert exc_info.value is failure
    assert len(client.list_calls) == 1
    assert [call["Key"] for call in client.get_calls] == keys
    assert [call["Key"] for call in client.delete_calls] == keys[
        : failure_index + 1
    ]


def test_fetch_does_not_delete_collected_candidates_after_later_read_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    keys = ["mail/newest", "mail/failing", "mail/oldest"]
    client = S3ClientFake(
        [
            {"Key": key, "LastModified": NOW - timedelta(minutes=index)}
            for index, key in enumerate(keys)
        ],
        {"mail/newest": _message()},
    )
    failure = RuntimeError("Synthetic later read failure")
    original_get = client.get_object

    def get_object(**kwargs: str) -> dict[str, BytesIO]:
        if kwargs["Key"] == "mail/failing":
            client.get_calls.append(kwargs)
            raise failure
        return original_get(**kwargs)

    async def unexpected_sleep(_delay: float) -> None:
        pytest.fail("Read failure must not trigger polling retry.")

    monkeypatch.setattr(client, "get_object", get_object)
    monkeypatch.setattr(s3_module.asyncio, "sleep", unexpected_sleep)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(provider.fetch(delete_read_emails=True))

    assert exc_info.value is failure
    assert len(client.list_calls) == 1
    assert [call["Key"] for call in client.get_calls] == keys[:2]
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


@pytest.mark.parametrize("delete_read_emails", [False, True])
def test_fetch_reports_missing_code_when_only_expired_email_exists(
    *,
    delete_read_emails: bool,
) -> None:
    client = S3ClientFake(
        [{"Key": "mail/expired", "LastModified": NOW - timedelta(hours=1)}],
        {"mail/expired": _message()},
    )
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    with pytest.raises(VerificationEmailNotFoundError):
        asyncio.run(
            provider.fetch_nowait(delete_read_emails=delete_read_emails)
        )

    expected_keys = ["mail/expired"] if delete_read_emails else []
    assert [call["Key"] for call in client.get_calls] == expected_keys
    assert [call["Key"] for call in client.delete_calls] == expected_keys
    assert len(client.list_calls) == 1


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


def test_fetch_cancellation_during_polling_stops_s3_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake([], {})
    delays: list[float] = []
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        poll_interval=7.0,
        client=cast("S3Client", client),
        clock=lambda: NOW,
    )

    async def scenario() -> None:
        waiting = asyncio.Event()
        release = asyncio.Event()

        async def wait_for_next_poll(delay: float) -> None:
            delays.append(delay)
            waiting.set()
            await release.wait()

        monkeypatch.setattr(s3_module.asyncio, "sleep", wait_for_next_poll)
        async with asyncio.TaskGroup() as group:
            task = group.create_task(provider.fetch(delete_read_emails=True))
            await waiting.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

    asyncio.run(scenario())

    assert delays == [7.0]
    assert len(client.list_calls) == 1
    assert client.get_calls == []
    assert client.delete_calls == []


@pytest.mark.parametrize("method_name", ["fetch", "fetch_nowait"])
def test_client_creation_failure_is_propagated_without_retry(
    method_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failure = RuntimeError("Synthetic client creation failure")
    profiles: list[str | None] = []

    def fail_creation(aws_profile: str | None) -> S3Client:
        profiles.append(aws_profile)
        raise failure

    async def unexpected_fetch_once(_client: S3Client, **_kwargs: bool) -> str:
        pytest.fail("Client creation failure must prevent S3 operations.")

    async def unexpected_sleep(_delay: float) -> None:
        pytest.fail("Client creation failure must not trigger polling retry.")

    monkeypatch.setattr(s3_module, "_create_s3_client", fail_creation)
    monkeypatch.setattr(s3_module.asyncio, "sleep", unexpected_sleep)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        aws_profile="example-profile",
        clock=lambda: NOW,
    )
    monkeypatch.setattr(provider, "_run_fetch_once", unexpected_fetch_once)

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(getattr(provider, method_name)())

    assert exc_info.value is failure
    assert profiles == ["example-profile"]


@pytest.mark.parametrize("method_name", ["fetch", "fetch_nowait"])
@pytest.mark.parametrize("inject_client", [False, True])
@pytest.mark.parametrize("fail_listing", [False, True])
def test_client_ownership_controls_cleanup(
    *,
    method_name: str,
    inject_client: bool,
    fail_listing: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    failure = RuntimeError("Synthetic listing failure")

    def create_client(_profile: str | None) -> S3Client:
        return cast("S3Client", client)

    def failed_listing(**_kwargs: str) -> dict[str, Any]:
        raise failure

    monkeypatch.setattr(s3_module, "_create_s3_client", create_client)
    if fail_listing:
        monkeypatch.setattr(client, "list_objects_v2", failed_listing)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        client=cast("S3Client", client) if inject_client else None,
        clock=lambda: NOW,
    )

    if fail_listing:
        with pytest.raises(RuntimeError) as exc_info:
            asyncio.run(getattr(provider, method_name)())
        assert exc_info.value is failure
    else:
        assert asyncio.run(getattr(provider, method_name)()) == "012345"
    assert client.close_calls == (0 if inject_client else 1)


@pytest.mark.parametrize("phase", ["creation", "operation"])
@pytest.mark.parametrize("repeat_cancel", [False, True])
def test_owned_client_is_closed_after_cancelled_thread_finishes(
    *,
    phase: str,
    repeat_cancel: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    release = threading.Event()
    original_close = client.close

    def checked_close() -> None:
        assert release.is_set(), "Client closed before its thread finished."
        original_close()

    monkeypatch.setattr(client, "close", checked_close)

    async def scenario() -> None:
        started = asyncio.Event()
        loop = asyncio.get_running_loop()
        original_list = client.list_objects_v2

        def wait_for_release() -> None:
            loop.call_soon_threadsafe(started.set)
            if not release.wait(10):
                msg = "Synthetic thread was not released."
                raise RuntimeError(msg)

        def create_client(_profile: str | None) -> S3Client:
            if phase == "creation":
                wait_for_release()
            return cast("S3Client", client)

        def list_objects(**kwargs: str) -> dict[str, Any]:
            wait_for_release()
            return original_list(**kwargs)

        monkeypatch.setattr(s3_module, "_create_s3_client", create_client)
        if phase == "operation":
            monkeypatch.setattr(client, "list_objects_v2", list_objects)
        provider = S3VerificationCodeProvider(
            email_address="user@example.com",
            bucket_name="example-bucket",
            clock=lambda: NOW,
        )
        async with asyncio.TaskGroup() as group:
            task = group.create_task(provider.fetch_nowait())
            try:
                async with asyncio.timeout(10):
                    await started.wait()
                task.cancel()
                await asyncio.sleep(0)
                if repeat_cancel:
                    task.cancel()
                    await asyncio.sleep(0)
                assert client.close_calls == 0
                assert not task.done()
            finally:
                release.set()
            with pytest.raises(asyncio.CancelledError):
                await task

    asyncio.run(scenario())
    assert client.close_calls == 1


@pytest.mark.parametrize("fail_listing", [False, True])
def test_owned_client_close_failure_preserves_operation_failure(
    *,
    fail_listing: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = S3ClientFake(
        [{"Key": "mail/valid", "LastModified": NOW}],
        {"mail/valid": _message()},
    )
    close_failure = RuntimeError("Synthetic client close failure")
    listing_failure = RuntimeError("Synthetic listing failure")

    def create_client(_profile: str | None) -> S3Client:
        return cast("S3Client", client)

    def close_client() -> None:
        client.close_calls += 1
        raise close_failure

    def failed_listing(**_kwargs: str) -> dict[str, Any]:
        raise listing_failure

    monkeypatch.setattr(s3_module, "_create_s3_client", create_client)
    monkeypatch.setattr(client, "close", close_client)
    if fail_listing:
        monkeypatch.setattr(client, "list_objects_v2", failed_listing)
    provider = S3VerificationCodeProvider(
        email_address="user@example.com",
        bucket_name="example-bucket",
        clock=lambda: NOW,
    )

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(provider.fetch_nowait())

    assert exc_info.value is close_failure
    if fail_listing:
        assert close_failure.__context__ is listing_failure
    assert client.close_calls == 1


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
        pytest.param(True, id="boolean-true"),
        pytest.param(False, id="boolean-false"),
        pytest.param(-1.0, id="negative"),
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
        pytest.param(1800.0, id="at-expiration"),
        pytest.param(1800.001, id="above-expiration"),
        pytest.param(10**400, id="integer-outside-float-range"),
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
