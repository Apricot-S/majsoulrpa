from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address

from majsoulrpa.exceptions import UserInputError
from majsoulrpa.netutils import UserPort


@dataclass(frozen=True)
class Config:
    browser_address: IPv4Address | IPv6Address
    remote_port: UserPort
    sniffer_port: UserPort

    def __post_init__(self) -> None:
        ports = [self.remote_port, self.sniffer_port]
        if len(set(ports)) != len(ports):
            msg = "port number conflict"
            raise UserInputError(msg)
