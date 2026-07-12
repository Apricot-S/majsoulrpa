import asyncio

from majsoulrpa.sniffer.events import DecodedSnifferMessage


class EmptySnifferMessageSource:
    async def get(self) -> DecodedSnifferMessage:
        future: asyncio.Future[DecodedSnifferMessage] = (
            asyncio.get_running_loop().create_future()
        )
        return await future

    def get_nowait(self) -> DecodedSnifferMessage | None:
        return None

    def put_back(self, message: DecodedSnifferMessage) -> None:
        _ = message


EMPTY_SNIFFER_MESSAGES = EmptySnifferMessageSource()
