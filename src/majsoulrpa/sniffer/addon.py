"""Addon for mitmproxy."""

import zmq.asyncio
from mitmproxy import addonmanager, ctx, http

from majsoulrpa import netutils
from majsoulrpa.constants import DEFAULT_CLIENT_ADDRESS, DEFAULT_SNIFFER_PORT


class Sniffer:
    def __init__(self) -> None:
        pass

    def load(self, loader: addonmanager.Loader) -> None:
        loader.add_option(
            name="address",
            typespec=str,
            default=DEFAULT_CLIENT_ADDRESS,
            help="IP address to send sniffed messages to",
        )
        loader.add_option(
            name="port",
            typespec=int,
            default=DEFAULT_SNIFFER_PORT,
            help="Port to send sniffed messages to",
        )

    def running(self) -> None:
        address_str: str = ctx.options.address
        port: int = ctx.options.port

        address = netutils.parse_ip_address(address_str)
        user_port = netutils.validate_user_port(port)
        endpoint = netutils.make_endpoint(address, user_port)

        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.PUB)

        if address.version == 6:  # noqa: PLR2004
            self._socket.setsockopt(zmq.IPV6, 1)

        self._socket.bind(f"tcp://{endpoint}")

    def done(self) -> None:
        self._socket.close()
        self._context.destroy()

    def websocket_message(self, flow: http.HTTPFlow) -> None:
        pass


addons = [Sniffer()]
