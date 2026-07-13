from datetime import UTC, datetime, timedelta
from email.message import EmailMessage

import pytest

from majsoulrpa.yostar import (
    InvalidYostarVerificationEmailError,
    extract_verification_code,
)

NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _message(
    *,
    sender: str = "info@passport.yostar.co.jp",
    recipient: str = "user@example.com",
    cc: str | None = None,
    subject: str = "【Yostar】メールアドレスの認証コードは　012345",
) -> bytes:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    if cc is not None:
        message["Cc"] = cc
    message["Subject"] = subject
    message.set_content("Synthetic test message.")
    return message.as_bytes()


def test_extracts_code_from_matching_message() -> None:
    assert (
        extract_verification_code(
            _message(),
            recipient="user@example.com",
            received_at=NOW - timedelta(minutes=1),
            now=NOW,
        )
        == "012345"
    )


@pytest.mark.parametrize(
    ("message", "received_at"),
    [
        (_message(sender="attacker@example.com"), NOW),
        (_message(recipient="other@example.com"), NOW),
        (
            _message(
                recipient="other@example.com",
                cc="user@example.com",
            ),
            NOW,
        ),
        (
            _message(subject="【Yostar】メールアドレスの認証コードは　12345"),
            NOW,
        ),
        (_message(), NOW - timedelta(minutes=30)),
    ],
)
def test_rejects_nonmatching_or_expired_message(
    message: bytes,
    received_at: datetime,
) -> None:
    with pytest.raises(InvalidYostarVerificationEmailError) as exc_info:
        extract_verification_code(
            message,
            recipient="user@example.com",
            received_at=received_at,
            now=NOW,
        )

    error = str(exc_info.value)
    assert "user@example.com" not in error
    assert "012345" not in error
