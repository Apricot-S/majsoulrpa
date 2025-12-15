from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import override


class CodeExtractorBase(ABC):
    @abstractmethod
    def extract_code(self, email_message: EmailMessage) -> str | None:
        pass


class CodeExtractor(CodeExtractorBase):
    @override
    def extract_code(self, email_message: EmailMessage) -> str | None:
        raise NotImplementedError
