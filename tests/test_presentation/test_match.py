# ruff: noqa: S101,SLF001
from unittest.mock import MagicMock, patch

import pytest

from majsoulrpa._impl.template import Template
from majsoulrpa.presentation.exceptions import InvalidOperationError
from majsoulrpa.presentation.match import MatchPresentation
from majsoulrpa.presentation.match.operation import LiqiOperation


class DummyMatchPresentation(MatchPresentation):
    def __init__(self) -> None:
        self._round_state = MagicMock()
        self._browser = MagicMock()

    def _dapai(self, index: int, forbidden_tiles: list[str]) -> None:
        pass


def test_operate_liqi() -> None:
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


def test_operate_liqi__after_kong() -> None:
    op = LiqiOperation(combinations=["0p"])
    assert op.candidate_dapai_list == ["0p"]

    with patch.object(
        Template,
        "open_file",
        return_value=MagicMock(),
    ):
        presentation = DummyMatchPresentation()
        # Case1: 1m is a kong
        presentation._round_state.shoupai = [  # type: ignore  # noqa: PGH003
            "2m",
            "2m",
            "2m",
            "3m",
            "3m",
            "3m",
            "5p",
            "0p",
            "6p",
            "1z",
        ]
        presentation._round_state.zimopai = "1z"  # type: ignore  # noqa: PGH003

        # valid index
        try:
            presentation._operate_liqi(op, 6)
            presentation._operate_liqi(op, 7)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        # invalid index
        for index in [0, 1, 2, 3, 4, 5, 8, 9, 10]:
            with pytest.raises(InvalidOperationError):
                presentation._operate_liqi(op, index)

        # Case2: Same as case1 but 1m and 2m are kong.
        presentation._round_state.shoupai = [  # type: ignore  # noqa: PGH003
            "3m",
            "3m",
            "3m",
            "5p",
            "0p",
            "6p",
            "1z",
        ]
        presentation._round_state.zimopai = "1z"  # type: ignore  # noqa: PGH003

        # valid index
        try:
            presentation._operate_liqi(op, 3)
            presentation._operate_liqi(op, 4)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        # invalid index
        for index in [0, 1, 2, 5, 6, 7]:
            with pytest.raises(InvalidOperationError):
                presentation._operate_liqi(op, index)

        # Case3: Same as case2 but 1m, 2m and 3m are kong.
        presentation._round_state.shoupai = [  # type: ignore  # noqa: PGH003
            "5p",
            "0p",
            "6p",
            "1z",
        ]
        presentation._round_state.zimopai = "1z"  # type: ignore  # noqa: PGH003

        # valid index
        try:
            presentation._operate_liqi(op, 0)
            presentation._operate_liqi(op, 1)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        # invalid index
        for index in [2, 3, 4]:
            with pytest.raises(InvalidOperationError):
                presentation._operate_liqi(op, index)

        # Case4: Same as case3 but 1m, 2m, 3m and 4m are kong.
        op = LiqiOperation(combinations=["0p", "1z"])
        assert op.candidate_dapai_list == ["0p", "1z"]
        presentation._round_state.shoupai = [  # type: ignore  # noqa: PGH003
            "5p",
        ]
        presentation._round_state.zimopai = "1z"  # type: ignore  # noqa: PGH003

        # valid index
        try:
            presentation._operate_liqi(op, 0)
            presentation._operate_liqi(op, 1)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")

        # invalid index
        with pytest.raises(InvalidOperationError):
            presentation._operate_liqi(op, 2)  # out-of-range
