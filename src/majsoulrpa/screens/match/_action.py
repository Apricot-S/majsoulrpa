import base64
import binascii
from collections.abc import Callable, Mapping

from google.protobuf.json_format import MessageToDict
from google.protobuf.message import DecodeError
from google.protobuf.message_factory import GetMessageClass
from pydantic import JsonValue

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match._decode import _get_int
from majsoulrpa.screens.match.event import (
    AngangEvent,
    BabeiEvent,
    ChiEvent,
    DaminggangEvent,
    DapaiEvent,
    HuleEvent,
    JiagangEvent,
    LiujuEvent,
    MatchEvent,
    NewRoundEvent,
    PengEvent,
    StartMatchEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)
from majsoulrpa.screens.match.operation._specification import (
    _OperationCandidatesSpecification,
)
from majsoulrpa.sniffer.events import DecodedNotice, Direction

ACTION_PROTOTYPE_NAME = ".lq.ActionPrototype"
_ACTION_DATA_KEYS = (132, 94, 78, 66, 57, 162, 31, 96, 28)
_ACTION_MESSAGE_TYPE_MAP = {
    f".{descriptor.full_name}": GetMessageClass(descriptor)
    for descriptor in liqi_pb2.DESCRIPTOR.message_types_by_name.values()
}

type _EventDecoder = Callable[[int, Mapping[str, JsonValue]], MatchEvent]


class MatchActionDecodeError(ValueError):
    pass


def _decode_chi_peng_gang_event(
    action_step: int,
    data: Mapping[str, JsonValue],
) -> MatchEvent:
    match _get_int(data, "ActionChiPengGang.type"):
        case 0:
            return ChiEvent.from_dict(action_step, data)
        case 1:
            return PengEvent.from_dict(action_step, data)
        case 2:
            return DaminggangEvent.from_dict(action_step, data)
        case _:
            msg = "ActionChiPengGang.type is not supported."
            raise ValueError(msg)


def _decode_angang_jiagang_event(
    action_step: int,
    data: Mapping[str, JsonValue],
) -> MatchEvent:
    match _get_int(data, "ActionAnGangAddGang.type"):
        case 2:
            return JiagangEvent.from_dict(action_step, data)
        case 3:
            return AngangEvent.from_dict(action_step, data)
        case _:
            msg = "ActionAnGangAddGang.type is not supported."
            raise ValueError(msg)


_EVENT_DECODERS: dict[str, _EventDecoder] = {
    "ActionMJStart": StartMatchEvent.from_dict,
    "ActionNewRound": NewRoundEvent.from_dict,
    "ActionDealTile": ZimoEvent.from_dict,
    "ActionDiscardTile": DapaiEvent.from_dict,
    "ActionChiPengGang": _decode_chi_peng_gang_event,
    "ActionAnGangAddGang": _decode_angang_jiagang_event,
    "ActionBaBei": BabeiEvent.from_dict,
    "ActionLiuJu": LiujuEvent.from_dict,
    "ActionHule": HuleEvent.from_dict,
}


def decode_live_action(
    message: DecodedNotice,
) -> tuple[
    MatchEvent,
    _OperationCandidatesSpecification | None,
    DecodedNotice,
]:
    if message.raw.direction is not Direction.INBOUND:
        msg = "A live action must be an inbound Notice."
        raise MatchActionDecodeError(msg)
    if message.raw.name != ACTION_PROTOTYPE_NAME:
        msg = "A live action must use .lq.ActionPrototype."
        raise MatchActionDecodeError(msg)
    event, operation, decoded_action = _decode_action(
        message.message,
        obfuscated=True,
    )
    return (
        event,
        operation,
        DecodedNotice(raw=message.raw, message=decoded_action),
    )


def decode_restore_action(
    action: Mapping[str, JsonValue],
) -> tuple[
    MatchEvent,
    _OperationCandidatesSpecification | None,
    dict[str, JsonValue],
]:
    return _decode_action(action, obfuscated=False)


def _decode_action(
    action: Mapping[str, JsonValue],
    *,
    obfuscated: bool,
) -> tuple[
    MatchEvent,
    _OperationCandidatesSpecification | None,
    dict[str, JsonValue],
]:
    step = action.get("step")
    name = action.get("name")
    encoded_data = action.get("data")
    if isinstance(step, bool) or not isinstance(step, int) or step < 0:
        msg = "Action step must be a nonnegative int."
        raise MatchActionDecodeError(msg)
    if not isinstance(name, str):
        msg = "Action name must be a string."
        raise MatchActionDecodeError(msg)
    event_decoder = _EVENT_DECODERS.get(name)
    if event_decoder is None:
        msg = "Action name is not supported."
        raise MatchActionDecodeError(msg)
    if not isinstance(encoded_data, str):
        msg = "Action data must be a base64 string."
        raise MatchActionDecodeError(msg)

    try:
        data = base64.b64decode(encoded_data, validate=True)
    except (binascii.Error, ValueError) as error:
        msg = "Action data is not valid base64."
        raise MatchActionDecodeError(msg) from error
    if obfuscated:
        data = _deobfuscate_action_data(data)

    message_type = _ACTION_MESSAGE_TYPE_MAP.get(f".lq.{name}")
    if message_type is None:
        msg = "Action type is absent from the protocol descriptor."
        raise MatchActionDecodeError(msg)
    protobuf_message = message_type()
    try:
        protobuf_message.ParseFromString(data)
    except DecodeError as error:
        msg = "Action protobuf data is malformed."
        raise MatchActionDecodeError(msg) from error
    decoded_data = MessageToDict(
        protobuf_message,
        always_print_fields_with_no_presence=True,
        preserving_proto_field_name=True,
    )

    decoded_action: dict[str, JsonValue] = {
        "step": step,
        "name": name,
        "data": decoded_data,
    }

    try:
        event = event_decoder(step, decoded_data)
        operation = decode_operation_specification(decoded_data)
    except (TypeError, ValueError) as error:
        msg = f"{name} fields are invalid."
        raise MatchActionDecodeError(msg) from error
    return event, operation, decoded_action


def _deobfuscate_action_data(data: bytes) -> bytes:
    result = bytearray(data)
    for index, value in enumerate(result):
        mask = (
            (23 ^ len(result))
            + 5 * index
            + _ACTION_DATA_KEYS[index % len(_ACTION_DATA_KEYS)]
        ) & 255
        result[index] = value ^ mask
    return bytes(result)
