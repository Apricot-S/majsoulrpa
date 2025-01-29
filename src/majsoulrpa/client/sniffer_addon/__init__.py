"""Add-ons for mitmproxy.

Sends messages sniffed by mitmproxy to a message queue.
"""

from pathlib import Path
from typing import Final

SNIFFER_ADDON_PATH: Final = Path(__file__).parent / "_zmq.py"
