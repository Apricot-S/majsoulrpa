import re
from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import override

VERIFICATION_CODE_PATTERN = re.compile(
    r"^【Yostar】メールアドレスの認証コードは　(\d{6})$",
)  # JP version
"""Regular expression for extracting a 6-digit verification code."""


class CodeExtractorBase(ABC):
    @abstractmethod
    def extract_code(self, mail: EmailMessage) -> str | None:
        pass


class CodeExtractor(CodeExtractorBase):
    def __init__(
        self,
        pattern: str | re.Pattern[str] = VERIFICATION_CODE_PATTERN,
    ) -> None:
        if isinstance(pattern, str):
            self._pattern = re.compile(pattern)
        else:
            self._pattern = pattern

    @override
    def extract_code(self, mail: EmailMessage) -> str | None:
        subject = mail.get("Subject")
        if subject is None:
            return None

        match = self._pattern.search(subject)
        return match.group(1) if match else None
