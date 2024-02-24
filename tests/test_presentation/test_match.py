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

        def _dapai(self, index: int, dapai: list[str]) -> None:
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
        presentation._round_state._zimopai = "1m"

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
