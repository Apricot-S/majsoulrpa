import datetime
import re
from abc import ABC, abstractmethod
from email.message import EmailMessage
from email.utils import parsedate_to_datetime
from enum import Enum, auto
from typing import override

YOSTAR_EMAIL_ADDRESS = "info@passport.yostar.co.jp"  # JP version
YOSTAR_EMAIL_SUBJECT_PATTERN = re.compile(
    r"^【Yostar】メールアドレスの認証コードは　\d{6}$",
)  # JP version
DEFAULT_EXPIRATION = datetime.timedelta(minutes=30)


class ClassificationResult(Enum):
    UNRELATED = auto()
    OBSOLETE = auto()
    VALID = auto()


class EmailClassifierBase(ABC):
    @property
    @abstractmethod
    def expiration(self) -> datetime.timedelta:
        pass

    @abstractmethod
    def classify(self, mail: EmailMessage) -> ClassificationResult:
        pass


class EmailClassifier(EmailClassifierBase):
    def __init__(
        self,
        sender: str = YOSTAR_EMAIL_ADDRESS,
        subject: re.Pattern[str] = YOSTAR_EMAIL_SUBJECT_PATTERN,
        expiration: datetime.timedelta = DEFAULT_EXPIRATION,
    ) -> None:
        self._sender = sender
        self._subject = subject
        self._expiration = expiration

    @property
    @override
    def expiration(self) -> datetime.timedelta:
        return self._expiration

    @override
    def classify(self, mail: EmailMessage) -> ClassificationResult:
        sender = mail.get("From")
        if sender is None or sender != self._sender:
            return ClassificationResult.UNRELATED

        subject = mail.get("Subject")
        if subject is None or not self._subject.match(subject):
            return ClassificationResult.UNRELATED

        raw_date = mail.get("Date")
        if raw_date is None:
            return ClassificationResult.UNRELATED
        try:
            date = parsedate_to_datetime(raw_date)
        except ValueError:
            return ClassificationResult.UNRELATED

        now = datetime.datetime.now(tz=datetime.UTC)
        if date < (now - self._expiration):
            return ClassificationResult.OBSOLETE

        return ClassificationResult.VALID
