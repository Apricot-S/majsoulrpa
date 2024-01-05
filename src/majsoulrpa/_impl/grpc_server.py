# ruff: noqa: ARG002, ANN001
import argparse
import asyncio

import grpc  # type:ignore[import-untyped]

from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2 import (
    BrowserRequest,
    BrowserResponse,
    Message,
    QueueSize,
    Timeout,
    Void,
)
from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2_grpc import (
    GRPCServerServicer,
    add_GRPCServerServicer_to_server,
)
from majsoulrpa.common import validate_user_port


class GRPCServer(GRPCServerServicer):
    def __init__(self) -> None:
        super().__init__()
        self._message_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._browser_request_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._browser_response_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def _push_impl(self, queue: asyncio.Queue[bytes], content: bytes) -> None:
        queue.put_nowait(content)

    def push_message(self, request: Message, context) -> Void:
        self._loop.run_in_executor(
            None,
            self._push_impl,
            self._message_queue,
            request.content,
        )
        return Void()

    def push_browser_request(
        self,
        request: BrowserRequest,
        context,
    ) -> Void:
        self._loop.run_in_executor(
            None,
            self._push_impl,
            self._browser_request_queue,
            request.content,
        )
        return Void()

    def push_browser_response(
        self,
        request: BrowserResponse,
        context,
    ) -> Void:
        self._loop.run_in_executor(
            None,
            self._push_impl,
            self._browser_response_queue,
            request.content,
        )
        return Void()

    async def _pop_impl(
        self,
        queue: asyncio.Queue[bytes],
        timeout: float,
    ) -> bytes:
        try:
            coro = asyncio.wait_for(queue.get(), timeout)
            result = await self._loop.create_task(coro)
        except TimeoutError:
            return b""
        else:
            return result

    def pop_message(self, request: Timeout, context) -> Message:
        result = self._loop.run_until_complete(
            self._pop_impl(self._message_queue, request.seconds),
        )
        return Message(content=result)

    def pop_browser_request(self, request: Timeout, context) -> BrowserRequest:
        result = self._loop.run_until_complete(
            self._pop_impl(self._browser_request_queue, request.seconds),
        )
        return BrowserRequest(content=result)

    def pop_browser_response(
        self,
        request: Timeout,
        context,
    ) -> BrowserResponse:
        result = self._loop.run_until_complete(
            self._pop_impl(self._browser_response_queue, request.seconds),
        )
        return BrowserResponse(content=result)

    def len_browser_request(self, request: Void, context) -> QueueSize:
        return QueueSize(size=self._browser_request_queue.qsize())


async def serve(port: int = 37247) -> None:
    server = grpc.aio.server()
    add_GRPCServerServicer_to_server(GRPCServer(), server)
    server.add_insecure_port(f"localhost:{port}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=37247)
    port: int = parser.parse_args().port
    validate_user_port(port)
    asyncio.run(serve(port))
