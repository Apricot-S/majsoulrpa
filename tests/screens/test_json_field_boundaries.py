from dataclasses import replace

import pytest

from majsoulrpa.screens._json_fields import JsonFieldDecodeError
from majsoulrpa.screens.match._metadata import (
    MatchMetadataDecodeError,
    decode_match_metadata,
)
from majsoulrpa.screens.room._decode import (
    RoomStateDecodeError,
    decode_room_state,
)
from tests.screens.match._support import SELF_ACCOUNT_ID, _auth_game


def test_room_field_failure_keeps_room_exception_boundary() -> None:
    with pytest.raises(RoomStateDecodeError, match=r"room\.room_id") as caught:
        decode_room_state({}, version=1, self_account_id=1)

    assert isinstance(caught.value.__cause__, JsonFieldDecodeError)


def test_metadata_field_failure_keeps_metadata_exception_boundary() -> None:
    message = replace(_auth_game(), request={"account_id": True})
    with pytest.raises(
        MatchMetadataDecodeError, match="authGame account_id"
    ) as caught:
        decode_match_metadata(message, SELF_ACCOUNT_ID)

    assert isinstance(caught.value.__cause__, JsonFieldDecodeError)
