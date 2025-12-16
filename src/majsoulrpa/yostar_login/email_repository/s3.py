from email.message import EmailMessage
from typing import Self, override

import aioboto3

from majsoulrpa.yostar_login.email_repository.base import EmailRepositoryBase


class S3EmailRepository(EmailRepositoryBase):
    def __init__(
        self,
        bucket_name: str,
        key_prefix: str,
        aws_profile: str | None,
    ) -> None:
        self._session = aioboto3.Session(profile_name=aws_profile)
        self._bucket_name = bucket_name
        self._key_prefix = key_prefix

    @override
    def __aiter__(self) -> Self:
        return self

    @override
    async def __anext__(self) -> tuple[str, EmailMessage]:
        raise NotImplementedError

    @override
    async def delete_message(self, key: str) -> None:
        async with self._session.client("s3") as s3_client:
            await s3_client.delete_object(Bucket=self._bucket_name, Key=key)
