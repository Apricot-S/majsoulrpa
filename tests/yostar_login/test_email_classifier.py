import datetime
from email.message import EmailMessage
from unittest.mock import MagicMock

import pytest

from majsoulrpa.yostar_login.email_classifier import (
    ClassificationResult,
    EmailClassifier,
)

_YOSTAR_EMAIL_ADDRESS = "info@passport.yostar.co.jp"
_YOSTAR_EMAIL_SUBJECT = "Eメールアドレスの確認"

_EXAMPLE_TO = "majsoulrpa-dev@example.com"


def make_mail(
    *,
    recipient: str | None = _EXAMPLE_TO,
    sender: str | None = _YOSTAR_EMAIL_ADDRESS,
    subject: str | None = _YOSTAR_EMAIL_SUBJECT,
    date: str | None = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["To"] = recipient
    msg["From"] = sender
    msg["Subject"] = subject
    if date:
        msg["Date"] = date
    return msg


def test_unrelated_from_mail_returns_unrelated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    date = "Tue, 16 Dec 2025 13:30:00 +0000"
    mail = make_mail(sender="someone@example.com", date=date)
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.UNRELATED


def test_unrelated_subject_mail_returns_unrelated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    date = "Tue, 16 Dec 2025 13:30:00 +0000"
    mail = make_mail(subject="Hello World", date=date)
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.UNRELATED


def test_mail_without_from_returns_unrelated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    date = "Tue, 16 Dec 2025 13:30:00 +0000"
    mail = make_mail(sender=None, date=date)
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.UNRELATED


def test_mail_without_subject_returns_unrelated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    date = "Tue, 16 Dec 2025 13:30:00 +0000"
    mail = make_mail(subject=None, date=date)
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.UNRELATED


def test_mail_without_date_returns_unrelated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    mail = make_mail(date=None)
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.UNRELATED


def test_mail_with_invalid_date_returns_unrelated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    mail = make_mail(date="not-a-date")
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.UNRELATED


def test_old_mail_returns_obsolete(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    mail = make_mail(date="Tue, 16 Dec 2025 13:29:59 +0000")
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.OBSOLETE


def test_mail_within_expiration_returns_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    mail = make_mail(date="Tue, 16 Dec 2025 13:30:00 +0000")
    classifier = EmailClassifier()
    result = classifier.classify(mail)
    assert result == ClassificationResult.VALID
