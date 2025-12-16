import email.policy
from collections.abc import AsyncIterator
from email.message import EmailMessage
from email.parser import BytesParser
from typing import override

import aioboto3

from majsoulrpa.yostar_login.email_repository.base import EmailRepositoryBase
from majsoulrpa.yostar_login.email_repository.config import S3Config


class S3EmailRepository(EmailRepositoryBase):
    def __init__(self, config: S3Config) -> None:
        self._session = aioboto3.Session(profile_name=config.aws_profile)
        self._bucket_name = config.bucket_name
        self._key_prefix = config.key_prefix

    @override
    async def iter_messages(self) -> AsyncIterator[tuple[str, EmailMessage]]:
        parser = BytesParser(policy=email.policy.SMTP)

        async with self._session.client("s3") as s3_client:
            resp = await s3_client.list_objects_v2(
                Bucket=self._bucket_name,
                Prefix=self._key_prefix,
            )

            for obj in resp.get("Contents", []):
                key = obj["Key"]  # pyright: ignore[reportTypedDictNotRequiredAccess]
                resp_obj = await s3_client.get_object(
                    Bucket=self._bucket_name,
                    Key=key,
                )
                body = await resp_obj["Body"].read()
                message = parser.parsebytes(body)
                yield key, message

    @override
    async def delete_message(self, key: str) -> None:
        async with self._session.client("s3") as s3_client:
            await s3_client.delete_object(Bucket=self._bucket_name, Key=key)
