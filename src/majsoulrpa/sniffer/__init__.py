from pathlib import Path

from majsoulrpa.sniffer.message_queue import MessageQueue, MessageQueueBase

ADDON_PATH = Path(__file__).parent / "addon.py"

__all__ = [
    "MessageQueue",
    "MessageQueueBase",
]

# submodules
__all__ += [
    "exceptions",  # type: ignore[reportUnsupportedDunderAll]
]
