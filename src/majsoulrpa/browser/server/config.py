from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address

from majsoulrpa import netutils
from majsoulrpa.exceptions import UserInputError


@dataclass(frozen=True)
class Config:
    client_address: IPv4Address | IPv6Address
    remote_port: int
    sniffer_port: int
    proxy_port: int

    def __post_init__(self) -> None:
        netutils.validate_user_port(self.remote_port)
        netutils.validate_user_port(self.sniffer_port)
        netutils.validate_user_port(self.proxy_port)

        ports = [self.remote_port, self.sniffer_port, self.proxy_port]
        if len(set(ports)) != len(ports):
            msg = "port number conflict"
            raise UserInputError(msg)
