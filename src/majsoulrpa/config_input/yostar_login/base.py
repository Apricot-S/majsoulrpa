from pydantic import BaseModel, ConfigDict

from majsoulrpa.config_input._common import _to_kebab
from majsoulrpa.config_input.yostar_login.s3 import S3


class YostarLogin(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_kebab,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    email_address: str | None = None
    s3: S3 | None = None
