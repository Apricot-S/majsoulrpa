import email.policy
from email.message import EmailMessage

import pytest

from majsoulrpa.yostar_login.code_extractor import CodeExtractor


def make_mail(subject: str) -> EmailMessage:
    msg = EmailMessage(policy=email.policy.SMTP)
    msg["Subject"] = subject
    return msg


def test_extract_code_success() -> None:
    mail = make_mail("【Yostar】メールアドレスの認証コードは　123456")
    extractor = CodeExtractor()
    assert extractor.extract_code(mail) == "123456"


@pytest.mark.parametrize(
    "text",
    [
        "",
        "【Yostar】メールアドレスの認証コードは　",
        "【Yostar】メールアドレスの認証コードは　12345",
        "【Yostar】メールアドレスの認証コードは　1234567",
        "【Yostar】メールアドレスの認証コードは 123456",
    ],
)
def test_extract_code_none(text: str) -> None:
    mail = make_mail(text)
    extractor = CodeExtractor()
    assert extractor.extract_code(mail) is None


def test_extract_code_custom_pattern() -> None:
    mail = make_mail("code: AB12CD34")
    extractor = CodeExtractor(r"([A-Z0-9]{8})")
    assert extractor.extract_code(mail) == "AB12CD34"
