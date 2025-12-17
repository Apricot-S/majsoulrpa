import email.policy
from email.message import EmailMessage

import pytest

from majsoulrpa.yostar_login.code_extractor import CodeExtractor


def make_mail(body: str) -> EmailMessage:
    msg = EmailMessage(policy=email.policy.SMTP)
    msg.set_content(body)
    return msg


def test_extract_code_success() -> None:
    mail = make_mail("<span style=3D>123456</span>")
    extractor = CodeExtractor()
    assert extractor.extract_code(mail) == "123456"


@pytest.mark.parametrize(
    "text",
    [
        "",
        "<span style=3D></span>",
        "<span style=3D>12345</span>",
        "<span style=3D>1234567</span>",
        "<span style=3D> 123456 </span>",
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
