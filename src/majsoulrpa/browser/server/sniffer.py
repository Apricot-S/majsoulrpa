import contextlib
import socket
import subprocess
import time
from pathlib import Path

from majsoulrpa.browser.server.config import Config
from majsoulrpa.netutils import UserPort


def wait_for_sniffer(
    port: UserPort,
    timeout: float,
    connect_timeout: float,
    interval: float,
) -> None:
    address = ("localhost", port)
    start = time.time()

    while True:
        with (
            contextlib.suppress(TimeoutError, ConnectionRefusedError),
            socket.create_connection(address, connect_timeout),
        ):
            return

        if time.time() - start > timeout:
            msg = f"sniffer proxy localhost:{port} did not open within {timeout} seconds"  # noqa: E501
            raise TimeoutError(msg)

        time.sleep(interval)


def run_sniffer(config: Config, addon_path: Path) -> subprocess.Popen:
    sniffer_args: list[str | Path] = [
        "mitmdump",
        "-q",
        "-p",
        str(config.proxy_port),
        "-s",
        addon_path,
        "--set",
        f"address={config.client_address}",
        "--set",
        f"port={config.sniffer_port}",
    ]
    sniffer_process = subprocess.Popen(sniffer_args)  # noqa: S603
    wait_for_sniffer(config.proxy_port, 5.0, 0.5, 0.5)
    return sniffer_process
