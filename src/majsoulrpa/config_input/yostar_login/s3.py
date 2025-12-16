from pydantic import BaseModel, ConfigDict

from majsoulrpa.config_input._common import _to_kebab


class S3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=_to_kebab,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    bucket_name: str
    key_prefix: str
    aws_profile: str | None = None
