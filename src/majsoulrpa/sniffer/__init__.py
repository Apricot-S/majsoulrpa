from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from majsoulrpa.sniffer.message_queue import MessageQueue, MessageQueueBase
else:
    try:
        from majsoulrpa.sniffer.message_queue import (
            MessageQueue,
            MessageQueueBase,
        )
    except ModuleNotFoundError:

        class _MessageQueueUnavailable:
            def __init__(self, *args, **kwargs) -> None:  # noqa: ARG002
                msg = "`MessageQueue` requires `client` extra"
                raise RuntimeError(msg)

        MessageQueue = _MessageQueueUnavailable  # type: ignore[assignment,misc]
        MessageQueueBase = _MessageQueueUnavailable  # type: ignore[assignment,misc]

ADDON_PATH = Path(__file__).parent / "addon.py"


__all__ = [
    "MessageQueue",
    "MessageQueueBase",
]
