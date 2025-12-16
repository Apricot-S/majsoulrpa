from majsoulrpa.yostar_login.code_extractor import (
    CodeExtractor,
    CodeExtractorBase,
)
from majsoulrpa.yostar_login.email_classifier import (
    EmailClassifier,
    EmailClassifierBase,
)
from majsoulrpa.yostar_login.email_repository import EmailRepositoryBase


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
