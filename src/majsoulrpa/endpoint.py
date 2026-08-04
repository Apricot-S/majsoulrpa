import ipaddress

from majsoulrpa.config import AppConfig


def make_browser_host_tcp_endpoint(config: AppConfig) -> str:
    return make_tcp_endpoint(
        host=config.endpoint.browser_host,
        port=config.endpoint.remote_port,
    )


def make_client_tcp_endpoint(config: AppConfig) -> str:
    return make_tcp_endpoint(
        host=config.endpoint.client_host,
        port=config.endpoint.remote_port,
    )


def make_sniffer_publisher_tcp_endpoint(config: AppConfig) -> str:
    return make_tcp_endpoint(
        host=config.endpoint.client_host,
        port=config.endpoint.sniffer_port,
    )


def make_sniffer_subscriber_tcp_endpoint(config: AppConfig) -> str:
    return make_tcp_endpoint(
        host=config.endpoint.browser_host,
        port=config.endpoint.sniffer_port,
    )


def make_tcp_endpoint(host: str, port: int) -> str:
    return f"tcp://{format_tcp_host(host)}:{port}"


def format_tcp_host(host: str) -> str:
    if is_ipv6_literal(host):
        return f"[{host}]"
    return host


def is_ipv6_literal(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return isinstance(address, ipaddress.IPv6Address)
