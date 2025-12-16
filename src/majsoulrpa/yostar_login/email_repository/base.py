from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import Self


class EmailRepositoryBase(ABC):
    @abstractmethod
    def __aiter__(self) -> Self:
        pass

    @abstractmethod
    async def __anext__(self) -> tuple[str, EmailMessage]:
        pass

    @abstractmethod
    async def delete_message(self, key: str) -> None:
        pass
