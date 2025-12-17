from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from email.message import EmailMessage


class EmailRepositoryBase(ABC):
    @abstractmethod
    async def iter_messages(self) -> AsyncIterator[tuple[str, EmailMessage]]:
        if False:
            yield "", EmailMessage()

    @abstractmethod
    async def delete_message(self, key: str) -> None:
        pass
