from email.message import EmailMessage
from typing import Self, override

import boto3

from majsoulrpa.yostar_login.email_repository.base import EmailRepositoryBase


class S3EmailRepository(EmailRepositoryBase):
    def __init__(
        self,
        bucket_name: str,
        key_prefix: str,
        aws_profile: str | None,
    ) -> None:
        session = boto3.Session(profile_name=aws_profile)
        s3_client = session.resource("s3")
        self._s3_bucket = s3_client.Bucket(bucket_name)
        self._key_prefix = key_prefix

    @override
    def __aiter__(self) -> Self:
        return self

    @override
    async def __anext__(self) -> tuple[str, EmailMessage]:
        raise NotImplementedError

    @override
    async def delete_message(self, key: str) -> None:
        self._s3_bucket.delete_objects(Delete={"Objects": [{"Key": key}]})
