from majsoulrpa.sniffer.events import DecodedSnifferMessage
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.screens._support import BrowserControllerSpy


class _MessagesOnClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        *messages_on_click: DecodedSnifferMessage,
    ) -> None:
        super().__init__(screenshot)
        self._messages = messages
        self._messages_on_click = messages_on_click

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        await super().click(x, y, warp=warp)
        for message in self._messages_on_click:
            self._messages.enqueue(message)


class _PrependTrackingQueue(SnifferMessageQueue):
    def __init__(self, *, max_payload_bytes: int = 1024) -> None:
        super().__init__(capacity=10, max_payload_bytes=max_payload_bytes)
        self.prepend_count = 0

    def prepend(self, message: DecodedSnifferMessage) -> None:
        self.prepend_count += 1
        super().prepend(message)


class _MessagesByClickBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        *messages_by_click: tuple[DecodedSnifferMessage, ...],
        allow_extra_clicks: bool,
    ) -> None:
        super().__init__(screenshot)
        self._messages = messages
        self._messages_by_click = list(messages_by_click)
        self._allow_extra_clicks = allow_extra_clicks

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> None:
        await super().click(x, y, warp=warp)
        if self._allow_extra_clicks and not self._messages_by_click:
            return
        for message in self._messages_by_click.pop(0):
            self._messages.enqueue(message)


class _MessageOnScreenshotBrowser(BrowserControllerSpy):
    def __init__(
        self,
        screenshot: bytes,
        messages: SnifferMessageQueue,
        message_on_screenshot: DecodedSnifferMessage,
    ) -> None:
        super().__init__(screenshot)
        self._messages = messages
        self._message_on_screenshot: DecodedSnifferMessage | None = (
            message_on_screenshot
        )

    async def screenshot(self) -> bytes:
        if self._message_on_screenshot is not None:
            self._messages.enqueue(self._message_on_screenshot)
            self._message_on_screenshot = None
        return await super().screenshot()
