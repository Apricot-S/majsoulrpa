import re
from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import override

VERIFICATION_CODE_PATTERN = re.compile(r">(\d{6})<")
"""Regular expression for extracting a 6-digit verification code.

The verification code is expected to be a 6-digit number enclosed
between HTML tags (e.g., `<span style=3D"">123456</span>`).
"""


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
        body_part = mail.get_body()
        if body_part is None:
            return None

        body = body_part.get_content()
        match = self._pattern.search(body)
        return match.group(1) if match else None
