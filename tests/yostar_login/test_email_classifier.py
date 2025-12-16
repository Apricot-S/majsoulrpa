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


def make_mail(
    sender: str | None,
    subject: str | None,
    date: str | None = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["Subject"] = subject
    if date:
        msg["Date"] = date
    return msg


def test_unrelated_from_mail_returns_unrelated() -> None:
    mail = make_mail("someone@example.com", _YOSTAR_EMAIL_SUBJECT)
    classifier = EmailClassifier()
    assert classifier.classify(mail) == ClassificationResult.UNRELATED


def test_unrelated_subject_mail_returns_unrelated() -> None:
    mail = make_mail(_YOSTAR_EMAIL_ADDRESS, "Hello World")
    classifier = EmailClassifier()
    assert classifier.classify(mail) == ClassificationResult.UNRELATED


def test_mail_without_from_returns_unrelated() -> None:
    mail = make_mail(None, _YOSTAR_EMAIL_SUBJECT)
    classifier = EmailClassifier()
    assert classifier.classify(mail) == ClassificationResult.UNRELATED


def test_mail_without_subject_returns_unrelated() -> None:
    mail = make_mail(_YOSTAR_EMAIL_ADDRESS, None)
    classifier = EmailClassifier()
    assert classifier.classify(mail) == ClassificationResult.UNRELATED


def test_mail_without_date_returns_unrelated() -> None:
    mail = make_mail(_YOSTAR_EMAIL_ADDRESS, _YOSTAR_EMAIL_SUBJECT, None)
    classifier = EmailClassifier()
    assert classifier.classify(mail) == ClassificationResult.UNRELATED


def test_old_mail_returns_obsolete(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed_now = datetime.datetime(2025, 12, 16, 14, 0, tzinfo=datetime.UTC)

    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = fixed_now
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    mail = make_mail(
        _YOSTAR_EMAIL_ADDRESS,
        _YOSTAR_EMAIL_SUBJECT,
        "Tue, 16 Dec 2025 13:29:59 +0000",
    )
    classifier = EmailClassifier()
    assert classifier.classify(mail) == ClassificationResult.OBSOLETE
