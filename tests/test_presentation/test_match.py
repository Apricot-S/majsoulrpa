# ruff: noqa: S101,SLF001
from unittest.mock import MagicMock, patch

import pytest

from majsoulrpa._impl.template import Template
from majsoulrpa.presentation.exceptions import InvalidOperationError
from majsoulrpa.presentation.match import MatchPresentation
from majsoulrpa.presentation.match.operation import LiqiOperation


def test_operate_liqi() -> None:
    class DummyMatchPresentation(MatchPresentation):
        def __init__(self) -> None:
            self._round_state = MagicMock()
            self._browser = MagicMock()

        def _dapai(self, index: int, forbidden_tiles: list[str]) -> None:
            pass

    op = LiqiOperation(combinations=["0s"])
    assert op.candidate_dapai_list == ["0s"]

    with patch.object(
        Template,
        "open_file",
        return_value=MagicMock(),
    ):
        presentation = DummyMatchPresentation()
        presentation._round_state.shoupai = [  # type: ignore  # noqa: PGH003
            "2m",
            "7m",
            "8m",
            "9m",
            "3p",
            "4p",
            "5p",
            "4s",
            "0s",  # <- index=8
            "5s",  # <- index=9
            "6s",
            "9s",
            "9s",
        ]
        presentation._round_state.zimopai = "1m"  # type: ignore  # noqa: PGH003

        try:
            presentation._operate_liqi(op, 8)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        try:
            presentation._operate_liqi(op, 9)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        with pytest.raises(InvalidOperationError):
            presentation._operate_liqi(op, 7)

        # Test to discard zimopai. 05s are only allowed to be discarded.
        with pytest.raises(InvalidOperationError):
            presentation._operate_liqi(op, 13)

        # Case2: Same hand but different zimopai.
        op = LiqiOperation(combinations=["0s"])
        assert op.candidate_dapai_list == ["0s"]

        presentation = DummyMatchPresentation()
        presentation._round_state.shoupai = [  # type: ignore  # noqa: PGH003
            "1m",
            "2m",
            "7m",
            "8m",
            "9m",
            "3p",
            "4p",
            "5p",
            "4s",
            "5s",  # <- index=9
            "6s",
            "9s",
            "9s",
        ]
        presentation._round_state.zimopai = "0s"  # type: ignore  # noqa: PGH003

        with pytest.raises(InvalidOperationError):
            presentation._operate_liqi(op, 8)

        try:
            presentation._operate_liqi(op, 9)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        # Test to discard zimopai. 05s are only allowed to be discarded.
        try:
            presentation._operate_liqi(op, 13)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        # Test Liqi operation without zimopai.
        presentation._round_state.zimopai = None  # type: ignore  # noqa: PGH003
        with pytest.raises(InvalidOperationError):
            presentation._operate_liqi(op, 9)
