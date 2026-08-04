import datetime

import pytest
from pydantic import JsonValue

from majsoulrpa.client.session import (
    AccountIDDecodeError,
    AccountIDMismatchError,
    SessionState,
)
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    Direction,
    RawNotice,
    RawRequestResponse,
)


def _request_response(
    name: str,
    response: dict[str, JsonValue],
) -> DecodedRequestResponse:
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    return DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=name,
            request=b"synthetic-request",
            response=b"synthetic-response",
            request_observed_at=observed_at,
            response_observed_at=observed_at,
        ),
        request={},
        response=response,
    )


def test_session_account_id_is_initially_none() -> None:
    assert SessionState().account_id is None


def test_session_extracts_account_id_from_oauth2_login() -> None:
    state = SessionState()

    state.observe(
        _request_response(
            ".lq.Lobby.oauth2Login",
            {"account_id": 123456},
        ),
    )

    assert state.account_id == 123456


def test_session_extracts_owner_id_from_created_room() -> None:
    state = SessionState()

    state.observe(
        _request_response(
            ".lq.Lobby.createRoom",
            {"room": {"owner_id": 123456}},
        ),
    )

    assert state.account_id == 123456


def test_session_ignores_messages_without_usable_account_id() -> None:
    state = SessionState()
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    notice = DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=".lq.Unrelated",
            payload=b"synthetic",
            observed_at=observed_at,
        ),
        message={},
    )

    state.observe(notice)
    state.observe(_request_response(".lq.Lobby.oauth2Login", {}))
    state.observe(
        _request_response(
            ".lq.Lobby.oauth2Login",
            {"account_id": 0},
        ),
    )
    state.observe(
        _request_response(
            ".lq.Lobby.oauth2Login",
            {"account_id": -1},
        ),
    )

    assert state.account_id is None


@pytest.mark.parametrize(
    ("name", "response"),
    [
        (".lq.Lobby.oauth2Login", {"account_id": True}),
        (".lq.Lobby.oauth2Login", {"account_id": "123456"}),
        (".lq.Lobby.oauth2Login", {"account_id": None}),
        (".lq.Lobby.createRoom", {"room": True}),
        (".lq.Lobby.createRoom", {"room": "invalid"}),
        (".lq.Lobby.createRoom", {"room": []}),
        (".lq.Lobby.createRoom", {"room": None}),
        (".lq.Lobby.createRoom", {"room": {"owner_id": True}}),
        (".lq.Lobby.createRoom", {"room": {"owner_id": "123456"}}),
        (".lq.Lobby.createRoom", {"room": {"owner_id": None}}),
    ],
)
def test_session_rejects_invalid_account_id_fields(
    name: str,
    response: dict[str, JsonValue],
) -> None:
    state = SessionState()

    with pytest.raises(AccountIDDecodeError):
        state.observe(_request_response(name, response))

    assert state.account_id is None


def test_session_allows_same_account_id_to_be_observed_again() -> None:
    state = SessionState()
    state.observe(
        _request_response(
            ".lq.Lobby.oauth2Login",
            {"account_id": 123456},
        ),
    )

    state.observe(
        _request_response(
            ".lq.Lobby.createRoom",
            {"room": {"owner_id": 123456}},
        ),
    )

    assert state.account_id == 123456


def test_session_rejects_inconsistent_account_id() -> None:
    state = SessionState()
    state.observe(
        _request_response(
            ".lq.Lobby.oauth2Login",
            {"account_id": 123456},
        ),
    )

    with pytest.raises(AccountIDMismatchError):
        state.observe(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": {"owner_id": 654321}},
            ),
        )

    assert state.account_id == 123456
