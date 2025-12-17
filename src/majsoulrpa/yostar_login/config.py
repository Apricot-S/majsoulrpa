from dataclasses import dataclass

from majsoulrpa.yostar_login.email_repository.config import S3Config


@dataclass(frozen=True)
class Config:
    email_address: str | None
    s3: S3Config | None
