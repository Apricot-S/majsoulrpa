import argparse
from queue import Empty, SimpleQueue
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


def start_server(port: int = 37247) -> None:
    server = SimpleXMLRPCServer(
        ("localhost", port),
        requestHandler=RequestHandler,
        allow_none=True,
        use_builtin_types=True,
    )

    message_queue: SimpleQueue[bytes] = SimpleQueue()

    def blpop(timeout: float) -> bytes | None:
        try:
            message = message_queue.get(timeout=timeout)
        except Empty:
            print(f"Empty. Size of message_queue: {message_queue.qsize()}")  # noqa: T201
            return None
        else:
            print(f"Popped. Size of message_queue: {message_queue.qsize()}")  # noqa: T201
            return message

    def rpush(value: bytes) -> None:
        message_queue.put(value)
        print(f"Pushed. Size of message_queue: {message_queue.qsize()}")  # noqa: T201

    server.register_instance(message_queue)
    server.register_function(blpop, "blpop")  # type: ignore[arg-type]
    server.register_function(rpush, "rpush") # type: ignore[arg-type]

    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=37247)
    port: int = parser.parse_args().port
    if (port < 1024) or (port > 49151):  # noqa: PLR2004
        msg = "Port number must be in the range 1024 to 49151."
        raise ValueError(msg)
    print(f"Listening on port {port}...")  # noqa: T201
    start_server(port)
