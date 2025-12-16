import pytest
from pydantic import ValidationError

from majsoulrpa.config_input.yostar_login.s3 import S3


def test_s3_from_dict_with_aliases() -> None:
    data = {
        "bucket-name": "my-bucket",
        "key-prefix": "logs/",
        "aws-profile": "dev",
    }
    s3 = S3.model_validate(data)

    assert s3.bucket_name == "my-bucket"
    assert s3.key_prefix == "logs/"
    assert s3.aws_profile == "dev"


def test_s3_from_dict_with_field_names() -> None:
    data = {
        "bucket_name": "my-bucket",
        "key_prefix": "logs/",
    }
    s3 = S3.model_validate(data)

    assert s3.bucket_name == "my-bucket"
    assert s3.key_prefix == "logs/"
    assert s3.aws_profile is None


def test_s3_serialize_by_alias() -> None:
    s3 = S3(bucket_name="my-bucket", key_prefix="logs/", aws_profile="dev")
    serialized = s3.model_dump()

    assert "bucket-name" in serialized
    assert "key-prefix" in serialized
    assert "aws-profile" in serialized
    assert serialized["bucket-name"] == "my-bucket"
    assert serialized["key-prefix"] == "logs/"
    assert serialized["aws-profile"] == "dev"


def test_s3_missing_required_bucket_name() -> None:
    data = {
        "key-prefix": "logs/",
        "aws-profile": "dev",
    }
    with pytest.raises(ValidationError):
        S3.model_validate(data)


def test_s3_missing_required_key_prefix() -> None:
    data = {
        "bucket-name": "my-bucket",
    }
    with pytest.raises(ValidationError):
        S3.model_validate(data)


def test_s3_missing_all_required_fields() -> None:
    data = {
        "aws-profile": "dev",
    }
    with pytest.raises(ValidationError):
        S3.model_validate(data)
