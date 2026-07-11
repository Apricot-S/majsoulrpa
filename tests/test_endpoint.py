from majsoulrpa.config import AppConfig, EndpointConfig
from majsoulrpa.endpoint import (
    format_tcp_host,
    make_browser_host_tcp_endpoint,
    make_client_tcp_endpoint,
    make_sniffer_publisher_tcp_endpoint,
    make_sniffer_subscriber_tcp_endpoint,
    make_tcp_endpoint,
)


def test_make_browser_host_tcp_endpoint_uses_browser_host() -> None:
    config = AppConfig(
        endpoint=EndpointConfig(
            browser_host="192.0.2.10",
            remote_port=12000,
        ),
    )

    assert make_browser_host_tcp_endpoint(config) == "tcp://192.0.2.10:12000"


def test_make_client_tcp_endpoint_uses_client_host() -> None:
    config = AppConfig(
        endpoint=EndpointConfig(
            client_host="192.0.2.20",
            remote_port=12000,
        ),
    )

    assert make_client_tcp_endpoint(config) == "tcp://192.0.2.20:12000"


def test_make_sniffer_publisher_endpoint_uses_client_host() -> None:
    config = AppConfig(
        endpoint=EndpointConfig(
            client_host="192.0.2.20",
            sniffer_port=12001,
        ),
    )

    assert (
        make_sniffer_publisher_tcp_endpoint(config) == "tcp://192.0.2.20:12001"
    )


def test_make_sniffer_subscriber_endpoint_uses_browser_host() -> None:
    config = AppConfig(
        endpoint=EndpointConfig(
            browser_host="192.0.2.10",
            sniffer_port=12001,
        ),
    )

    assert (
        make_sniffer_subscriber_tcp_endpoint(config)
        == "tcp://192.0.2.10:12001"
    )


def test_make_tcp_endpoint_brackets_ipv6_literal() -> None:
    assert make_tcp_endpoint(host="::1", port=12000) == "tcp://[::1]:12000"


def test_format_tcp_host_keeps_hostname() -> None:
    assert format_tcp_host("browser-host.local") == "browser-host.local"
