import logging
from datetime import UTC, datetime, timedelta, timezone, tzinfo
from email.message import EmailMessage

import pytest

from majsoulrpa.yostar_email import (
    InvalidYostarVerificationEmailError,
    YostarVerificationEmailError,
    extract_verification_code,
)
from majsoulrpa.yostar_email.email import VerificationEmail

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


class UndefinedOffsetTimezone(tzinfo):
    def utcoffset(self, _dt: datetime | None) -> None:
        return None

    def dst(self, _dt: datetime | None) -> None:
        return None

    def tzname(self, _dt: datetime | None) -> None:
        return None


class ChangingOffsetTimezone(tzinfo):
    """Synthetic offset transition at local hour 3."""

    def __init__(self, before: int, after: int) -> None:
        self.before = timedelta(hours=before)
        self.after = timedelta(hours=after)

    def utcoffset(self, dt: datetime | None) -> timedelta | None:
        if dt is None:
            return None
        return self.before if dt.hour < 3 else self.after

    def dst(self, _dt: datetime | None) -> timedelta:
        return timedelta(0)

    def tzname(self, _dt: datetime | None) -> str:
        return "Synthetic"


@pytest.mark.parametrize(
    ("before", "after", "received_hour", "expected_age"),
    [
        pytest.param(1, 2, 1, timedelta(minutes=20), id="forward-valid"),
        pytest.param(2, 1, 2, timedelta(minutes=80), id="backward-expired"),
        pytest.param(1, 2, 2, timedelta(minutes=-40), id="forward-future"),
    ],
)
def test_validity_uses_utc_elapsed_time_with_same_changing_timezone(
    before: int,
    after: int,
    received_hour: int,
    expected_age: timedelta,
) -> None:
    zone = ChangingOffsetTimezone(before, after)
    received_at = NOW.replace(hour=received_hour, minute=50, tzinfo=zone)
    current_time = NOW.replace(hour=3, minute=10, tzinfo=zone)
    assert (
        current_time.astimezone(UTC) - received_at.astimezone(UTC)
        == expected_age
    )

    if timedelta(0) <= expected_age < timedelta(minutes=30):
        assert (
            extract_verification_code(
                _message(),
                recipient="user@example.com",
                received_at=received_at,
                now=current_time,
            )
            == "012345"
        )
    else:
        with pytest.raises(InvalidYostarVerificationEmailError):
            extract_verification_code(
                _message(),
                recipient="user@example.com",
                received_at=received_at,
                now=current_time,
            )


@pytest.mark.parametrize(
    "timestamp",
    [
        pytest.param(NOW.replace(tzinfo=None), id="no-tzinfo"),
        pytest.param(
            NOW.replace(tzinfo=UndefinedOffsetTimezone()),
            id="undefined-utc-offset",
        ),
    ],
)
@pytest.mark.parametrize("field_name", ["now", "received_at"])
def test_rejects_timestamp_without_defined_utc_offset(
    timestamp: datetime,
    field_name: str,
) -> None:
    with pytest.raises(ValueError, match="timezone information") as exc_info:
        extract_verification_code(
            _message(),
            recipient="user@example.com",
            received_at=timestamp if field_name == "received_at" else NOW,
            now=timestamp if field_name == "now" else NOW,
        )

    for output in (str(exc_info.value), repr(exc_info.value)):
        assert "user@example.com" not in output
        assert "012345" not in output


@pytest.mark.parametrize(
    "age",
    [
        pytest.param(timedelta(minutes=29), id="valid-age"),
        pytest.param(timedelta(minutes=30), id="expired-age"),
    ],
)
def test_validity_uses_elapsed_time_across_utc_offsets(age: timedelta) -> None:
    received_at = (NOW - age).astimezone(timezone(timedelta(hours=9)))

    if age < timedelta(minutes=30):
        assert (
            extract_verification_code(
                _message(),
                recipient="user@example.com",
                received_at=received_at,
                now=NOW,
            )
            == "012345"
        )
    else:
        with pytest.raises(InvalidYostarVerificationEmailError):
            extract_verification_code(
                _message(),
                recipient="user@example.com",
                received_at=received_at,
                now=NOW,
            )


@pytest.mark.parametrize("header_name", ["Subject", "subject"])
def test_duplicate_subject_is_not_a_code_or_deletion_candidate(
    header_name: str,
) -> None:
    message = _message().replace(
        b"\n\n",
        f"\n{header_name}: Synthetic duplicate subject\n\n".encode(),
        1,
    )
    email = VerificationEmail.parse(message)

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError, match="subject"):
        email.extract_code(recipient="user@example.com")


def test_missing_subject_is_not_a_code_or_deletion_candidate() -> None:
    message = EmailMessage()
    message["From"] = "info@passport.yostar.co.jp"
    message["To"] = "user@example.com"
    message.set_content("Synthetic test message.")
    email = VerificationEmail.parse(message.as_bytes())

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError, match="subject"):
        email.extract_code(recipient="user@example.com")


@pytest.mark.parametrize(
    "charset",
    [
        pytest.param(b"unknown-charset", id="unknown-charset"),
        pytest.param(b"ascii", id="bytes-invalid-for-declared-charset"),
    ],
)
def test_bad_subject_encoding_cannot_supply_code_or_allow_deletion(
    charset: bytes,
) -> None:
    message = _message().replace(b"=?utf-8?", b"=?" + charset + b"?", 1)
    email = VerificationEmail.parse(message)

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError, match="subject"):
        email.extract_code(recipient="user@example.com")


@pytest.mark.parametrize(
    ("original", "replacement"),
    [
        pytest.param(
            b"\n\n",
            b"\nSynthetic malformed header line\n\n",
            id="missing-header-body-separator",
        ),
        pytest.param(
            b'Content-Type: text/plain; charset="utf-8"',
            b'Content-Type: multipart/mixed; boundary="synthetic-boundary"',
            id="missing-multipart-boundary",
        ),
    ],
)
def test_malformed_mime_structure_cannot_supply_code_or_allow_deletion(
    original: bytes,
    replacement: bytes,
) -> None:
    email = VerificationEmail.parse(
        _message().replace(original, replacement, 1)
    )

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError):
        email.extract_code(recipient="user@example.com")


def test_well_formed_multipart_email_supplies_code_and_allows_deletion() -> (
    None
):
    message = EmailMessage()
    message["From"] = "info@passport.yostar.co.jp"
    message["To"] = "user@example.com"
    message["Subject"] = "【Yostar】メールアドレスの認証コードは　012345"
    message.set_content("Synthetic text body.")
    message.add_alternative("<p>Synthetic HTML body.</p>", subtype="html")
    email = VerificationEmail.parse(message.as_bytes())

    assert email.extract_code(recipient="user@example.com") == "012345"
    assert email.matches_deletion_condition(recipient="user@example.com")


@pytest.mark.parametrize(
    "from_headers",
    [
        pytest.param(b"", id="missing-from"),
        pytest.param(
            b"From: info@passport.yostar.co.jp\n"
            b"from: info@passport.yostar.co.jp\n",
            id="duplicate-from",
        ),
        pytest.param(
            b"From: info@passport.yostar.co.jp, other@example.com\n",
            id="multiple-senders",
        ),
        pytest.param(
            b"From: Yostar <info@passport.yostar.co.jp\n",
            id="missing-closing-angle-bracket",
        ),
    ],
)
def test_invalid_from_cannot_supply_code_but_keeps_deletion_condition(
    from_headers: bytes,
) -> None:
    email = VerificationEmail.parse(
        _message().replace(
            b"From: info@passport.yostar.co.jp\n", from_headers, 1
        )
    )

    with pytest.raises(InvalidYostarVerificationEmailError, match="sender"):
        email.extract_code(recipient="user@example.com")
    assert email.matches_deletion_condition(recipient="user@example.com")


def test_accepts_sender_with_display_name() -> None:
    email = VerificationEmail.parse(
        _message(sender="Yostar <info@passport.yostar.co.jp>")
    )

    assert email.extract_code(recipient="user@example.com") == "012345"


@pytest.mark.parametrize(
    "extra_header",
    [
        pytest.param(b"To: other@example.com", id="duplicate-to"),
        pytest.param(b"to: user@example.com", id="duplicate-lowercase-to"),
    ],
)
def test_duplicate_to_is_not_a_code_or_deletion_candidate(
    extra_header: bytes,
) -> None:
    message = _message().replace(b"\n\n", b"\n" + extra_header + b"\n\n", 1)
    email = VerificationEmail.parse(message)

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError, match="recipient"):
        email.extract_code(recipient="user@example.com")


def test_missing_to_is_not_a_code_or_deletion_candidate() -> None:
    email = VerificationEmail.parse(
        _message().replace(b"To: user@example.com\n", b"", 1)
    )

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError, match="recipient"):
        email.extract_code(recipient="user@example.com")


def test_single_to_can_contain_multiple_recipients() -> None:
    email = VerificationEmail.parse(
        _message(recipient="other@example.com, User <user@example.com>")
    )

    assert email.extract_code(recipient="user@example.com") == "012345"
    assert email.matches_deletion_condition(recipient="user@example.com")


def test_malformed_to_is_not_a_code_or_deletion_candidate() -> None:
    email = VerificationEmail.parse(
        _message().replace(
            b"To: user@example.com\n",
            b"To: User <user@example.com\n",
            1,
        )
    )

    assert not email.matches_deletion_condition(recipient="user@example.com")
    with pytest.raises(InvalidYostarVerificationEmailError, match="recipient"):
        email.extract_code(recipient="user@example.com")


def test_parsed_email_representation_and_logs_hide_email_data(
    caplog: pytest.LogCaptureFixture,
) -> None:
    email = VerificationEmail.parse(_message())

    with caplog.at_level(logging.INFO):
        logging.getLogger(__name__).info("Parsed email: %s / %r", email, email)

    for output in (repr(email), str(email), caplog.text):
        for value in (
            "info@passport.yostar.co.jp",
            "user@example.com",
            "012345",
            "Synthetic test message.",
        ):
            assert value not in output

    assert email.extract_code(recipient="user@example.com") == "012345"
    assert email.matches_deletion_condition(recipient="user@example.com")


@pytest.mark.parametrize(
    "age",
    [
        pytest.param(timedelta(0), id="received-now"),
        pytest.param(
            timedelta(minutes=30) - timedelta(microseconds=1),
            id="just-before-expiration",
        ),
    ],
)
def test_extracts_code_from_matching_message(age: timedelta) -> None:
    assert (
        extract_verification_code(
            _message(),
            recipient="user@example.com",
            received_at=NOW - age,
            now=NOW,
        )
        == "012345"
    )


@pytest.mark.parametrize(
    "subject",
    [
        pytest.param(
            "【Yostar】メールアドレスの認証コードは　０１２３４５",  # noqa: RUF001
            id="fullwidth-digits",
        ),
        pytest.param(
            "【Yostar】メールアドレスの認証コードは　٠١٢٣٤٥",
            id="arabic-indic-digits",
        ),
        pytest.param(
            "【Yostar】メールアドレスの認証コードは　0123456",
            id="seven-digits",
        ),
        pytest.param(
            "【Yostar】メールアドレスの認証コードは 012345",
            id="ascii-space",
        ),
        pytest.param(
            "prefix【Yostar】メールアドレスの認証コードは　012345",
            id="extra-prefix",
        ),
        pytest.param(
            "【Yostar】メールアドレスの認証コードは　012345suffix",
            id="extra-suffix",
        ),
    ],
)
def test_rejects_subject_outside_known_ascii_code_format(subject: str) -> None:
    with pytest.raises(InvalidYostarVerificationEmailError, match="subject"):
        extract_verification_code(
            _message(subject=subject),
            recipient="user@example.com",
            received_at=NOW,
            now=NOW,
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
        pytest.param(
            _message(),
            NOW + timedelta(microseconds=1),
            id="future-received-time",
        ),
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

    assert isinstance(exc_info.value, YostarVerificationEmailError)
    for error in (str(exc_info.value), repr(exc_info.value)):
        for value in (
            "user@example.com",
            "other@example.com",
            "attacker@example.com",
            "012345",
            "Synthetic test message.",
        ):
            assert value not in error
