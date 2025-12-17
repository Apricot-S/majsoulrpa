from majsoulrpa.config_input.yostar_login import YostarLogin
from majsoulrpa.config_input.yostar_login.s3 import S3


def test_yostar_login_empty_ok() -> None:
    login = YostarLogin.model_validate({})
    assert login.email_address is None
    assert login.s3 is None


def test_yostar_login_with_email_only() -> None:
    data = {
        "email-address": "user@example.com",
    }
    login = YostarLogin.model_validate(data)
    assert login.email_address == "user@example.com"
    assert login.s3 is None


def test_yostar_login_with_nested_s3() -> None:
    data = {
        "s3": {
            "bucket-name": "my-bucket",
            "key-prefix": "logs/",
            "aws-profile": "dev",
        },
    }
    login = YostarLogin.model_validate(data)
    assert login.email_address is None
    assert isinstance(login.s3, S3)
    assert login.s3.bucket_name == "my-bucket"
    assert login.s3.key_prefix == "logs/"
    assert login.s3.aws_profile == "dev"


def test_yostar_login_serialize_by_alias() -> None:
    login = YostarLogin(
        email_address="user@example.com",
        s3=S3(bucket_name="my-bucket", key_prefix="logs/"),
    )
    serialized = login.model_dump()

    assert "email-address" in serialized
    assert "s3" in serialized
    assert "bucket-name" in serialized["s3"]
    assert "key-prefix" in serialized["s3"]


def test_yostar_login_ignore_extra_fields() -> None:
    data = {
        "email-address": "user@example.com",
        "s3": {
            "bucket-name": "my-bucket",
            "key-prefix": "logs/",
        },
        "imap-settings": {"host": "imap.example.com"},
        "gmail-api-token": "dummy-token",
    }
    login = YostarLogin.model_validate(data)

    assert login.email_address == "user@example.com"
    assert isinstance(login.s3, S3)
    assert login.s3.bucket_name == "my-bucket"

    serialized = login.model_dump(by_alias=True)
    assert "imap-settings" not in serialized
    assert "gmail-api-token" not in serialized
