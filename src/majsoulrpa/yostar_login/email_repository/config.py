from dataclasses import dataclass


@dataclass(frozen=True)
class S3Config:
    bucket_name: str
    key_prefix: str
    aws_profile: str | None
