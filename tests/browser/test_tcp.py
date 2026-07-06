import asyncio

from majsoulrpa.browser import (
    BrowserCommand,
    BrowserResponse,
    BrowserTcpServer,
    ClickCommand,
    ClickResponse,
    TextInputCommand,
    TextInputResponse,
)
from majsoulrpa.browser.tcp import ClientConnectedCallback


class RecordingExecutor:
    def __init__(self) -> None:
        self.commands: list[BrowserCommand] = []

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        self.commands.append(command)
        match command:
            case ClickCommand(x=x, y=y):
                return ClickResponse(x=x, y=y)
            case TextInputCommand(text=text):
                return TextInputResponse(text=text)
            case _:
                msg = "unexpected command"
                raise AssertionError(msg)


async def _roundtrip_two_commands() -> None:
    executor = RecordingExecutor()
    server = BrowserTcpServer(
        host="127.0.0.1",
        port=0,
        executor=executor,
    )
    await server.bind()
    try:
        address = server.address
        reader, writer = await asyncio.open_connection(
            address.host,
            address.port,
        )

        writer.write(
            b'{"type":"click","x":25,"y":40,'
            b'"mouse_down_up_delay_seconds":0.1}\n',
        )
        await writer.drain()
        assert await reader.readline() == (
            b'{"type":"click","x":25.0,"y":40.0}\n'
        )

        writer.write(
            b'{"type":"text_input","text":"abc",'
            b'"character_delay_seconds":0.05}\n',
        )
        await writer.drain()
        assert await reader.readline() == (
            b'{"type":"text_input","text":"abc"}\n'
        )

        writer.close()
        await writer.wait_closed()
    finally:
        await server.stop()

    assert executor.commands == [
        ClickCommand(
            x=25,
            y=40,
            mouse_down_up_delay_seconds=0.1,
        ),
        TextInputCommand(
            text="abc",
            character_delay_seconds=0.05,
        ),
    ]


def test_browser_tcp_server_processes_json_stream_client() -> None:
    asyncio.run(_roundtrip_two_commands())


class ClosingServer:
    def __init__(self) -> None:
        self.closed = False
        self.wait_closed_called = False

    @property
    def sockets(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True

    async def serve_forever(self) -> None:
        raise asyncio.CancelledError

    async def wait_closed(self) -> None:
        self.wait_closed_called = True


async def _start_server_factory(
    *,
    host: str,
    port: int,
    executor: RecordingExecutor,
    closing_server: ClosingServer,
) -> None:
    async def start_server(
        client_connected_cb: ClientConnectedCallback,
        server_host: str,
        server_port: int,
    ) -> ClosingServer:
        _ = client_connected_cb
        assert server_host == host
        assert server_port == port
        return closing_server

    server = BrowserTcpServer(
        host=host,
        port=port,
        executor=executor,
        start_server=start_server,
    )
    await server.bind()
    await server.stop()


def test_browser_tcp_server_stops_underlying_server() -> None:
    closing_server = ClosingServer()

    asyncio.run(
        _start_server_factory(
            host="127.0.0.1",
            port=29200,
            executor=RecordingExecutor(),
            closing_server=closing_server,
        ),
    )

    assert closing_server.closed
    assert closing_server.wait_closed_called
