import asyncio
from collections.abc import Iterable
from datetime import UTC, datetime
from email.message import EmailMessage
from email.utils import parsedate_to_datetime
from itertools import chain
from logging import getLogger
from typing import assert_never

from majsoulrpa.yostar_login.code_extractor import (
    CodeExtractor,
    CodeExtractorBase,
)
from majsoulrpa.yostar_login.email_classifier import (
    ClassificationResult,
    EmailClassifier,
    EmailClassifierBase,
)
from majsoulrpa.yostar_login.email_repository import EmailRepositoryBase

logger = getLogger(__name__)


class YostarLogin:
    def __init__(
        self,
        repository: EmailRepositoryBase,
        classifier: EmailClassifierBase | None = None,
        extractor: CodeExtractorBase | None = None,
    ) -> None:
        self._repository = repository
        if classifier is None:
            self._classifier: EmailClassifierBase = EmailClassifier()
        else:
            self._classifier = classifier
        if extractor is None:
            self._extractor: CodeExtractorBase = CodeExtractor()
        else:
            self._extractor = extractor

        self._background_tasks: set[asyncio.Task] = set()

    async def fetch_code(
        self,
        to: str,
        sent_at: datetime,
        *,
        retry_interval: float = 5.0,
        cleanup: bool = False,
    ) -> str | None:
        deadline = sent_at + self._classifier.expiration

        code: str | None = None
        while datetime.now(UTC) < deadline:
            (
                valid_candidates,
                deletion_targets,
            ) = await self._collect_candidates(to, sent_at)

            if valid_candidates:
                _, latest_message = self._select_latest(valid_candidates)
                code = self._extractor.extract_code(latest_message)

            if cleanup and (valid_candidates or deletion_targets):
                coro = self._cleanup(chain(valid_candidates, deletion_targets))
                task = asyncio.create_task(coro)
                self._background_tasks.add(task)
                task.add_done_callback(self._background_tasks.discard)

            if code is not None:
                logger.debug("Fetched verification code: %s", code)
                return code

            logger.debug(
                "No verification code yet, retrying in %.1f sec",
                retry_interval,
            )
            await asyncio.sleep(retry_interval)

        logger.warning("Failed to fetch verification code within expiration.")
        return None

    async def _collect_candidates(
        self,
        to: str,
        sent_at: datetime,
    ) -> tuple[dict[str, EmailMessage], dict[str, EmailMessage]]:
        valid_candidates: dict[str, EmailMessage] = {}
        deletion_targets: dict[str, EmailMessage] = {}

        async for key, message in self._repository.iter_messages():
            recipient = message.get("To")
            if recipient is None or recipient != to:
                continue

            match self._classifier.classify(message):
                case ClassificationResult.UNRELATED:
                    continue
                case ClassificationResult.OBSOLETE:
                    deletion_targets[key] = message
                case ClassificationResult.VALID:
                    date = parsedate_to_datetime(message["Date"])
                    if date >= sent_at:
                        valid_candidates[key] = message
                    else:
                        deletion_targets[key] = message
                case _ as unreachable:
                    assert_never(unreachable)

        return (valid_candidates, deletion_targets)

    def _select_latest(
        self,
        valid_candidates: dict[str, EmailMessage],
    ) -> tuple[str, EmailMessage]:
        return max(
            valid_candidates.items(),
            key=lambda item: parsedate_to_datetime(item[1]["Date"]),
        )

    async def _cleanup(self, deletion_targets: Iterable[str]) -> None:
        for key in deletion_targets:
            logger.debug("Attempting to delete message with key: %s", key)
            try:
                await self._repository.delete_message(key)
                logger.info("Successfully deleted message with key: %s", key)
            except Exception:
                logger.exception("Failed to delete message with key: %s", key)
