import base64
import datetime

from majsoulrpa.sniffer.events import DecodedNotice, Direction, RawNotice

OBSERVED_AT = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)


def _obfuscate_action_data(data: bytes) -> bytes:
    keys = (132, 94, 78, 66, 57, 162, 31, 96, 28)
    result = bytearray(data)
    for index, value in enumerate(result):
        mask = (
            (23 ^ len(result)) + 5 * index + keys[index % len(keys)]
        ) & 0xFF
        result[index] = value ^ mask
    return bytes(result)


def _live_action(
    *,
    step: int = 0,
    name: str = "ActionMJStart",
    data: bytes = b"",
) -> DecodedNotice:
    encoded_data = base64.b64encode(_obfuscate_action_data(data)).decode()
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=".lq.ActionPrototype",
            payload=b"synthetic-action",
            observed_at=OBSERVED_AT,
        ),
        message={"step": step, "name": name, "data": encoded_data},
    )
