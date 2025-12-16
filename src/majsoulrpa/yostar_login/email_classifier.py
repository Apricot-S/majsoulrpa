from abc import ABC, abstractmethod
from email.message import EmailMessage
from enum import Enum, auto
from typing import override

YOSTAR_EMAIL_ADDRESS = "info@passport.yostar.co.jp"  # JP version
YOSTAR_EMAIL_SUBJECT = "Eメールアドレスの確認"  # JP version


class ClassificationResult(Enum):
    UNRELATED = auto()
    OBSOLETE = auto()
    VALID = auto()


class EmailClassifierBase(ABC):
    @abstractmethod
    def classify(self, mail: EmailMessage) -> ClassificationResult:
        pass


class EmailClassifier(EmailClassifierBase):
    def __init__(
        self,
        sender: str = YOSTAR_EMAIL_ADDRESS,
        subject: str = YOSTAR_EMAIL_SUBJECT,
    ) -> None:
        self._sender = sender
        self._subject = subject

    @override
    def classify(self, mail: EmailMessage) -> ClassificationResult:
        sender = mail.get("From")
        if sender is None or sender != self._sender:
            return ClassificationResult.UNRELATED

        subject = mail.get("Subject")
        if subject is None or subject != self._subject:
            return ClassificationResult.UNRELATED

        date = mail.get("Date")
        if date is None:
            return ClassificationResult.UNRELATED

        return ClassificationResult.OBSOLETE
