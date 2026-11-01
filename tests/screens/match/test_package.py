import subprocess
import sys
import textwrap

import pytest

from majsoulrpa.screens import match as package
from majsoulrpa.screens.match import event, operation, state, types


def test_public_exports_preserve_defining_objects() -> None:
    state_names = {
        "Angang",
        "Babei",
        "Chi",
        "Daminggang",
        "Dapai",
        "Fulu",
        "Jiagang",
        "MatchOrigin",
        "MatchPlayer",
        "MatchRank",
        "MatchState",
        "Peng",
        "RoundState",
    }
    type_names = {"Seat", "Tile", "validate_seat", "validate_tile"}
    expected = {
        **{name: getattr(state, name) for name in state_names},
        **{name: getattr(types, name) for name in type_names},
        **{name: getattr(event, name) for name in event.__all__},
        **{name: getattr(operation, name) for name in operation.__all__},
    }

    assert set(package.__all__) == expected.keys() | {"MatchScreen"}
    for name, value in expected.items():
        assert getattr(package, name) is value
    private_name = "_OperationCandidatesSpecification"
    with pytest.raises(AttributeError):
        getattr(package, private_name)


def test_value_imports_do_not_load_screen_or_optional_dependencies() -> None:
    script = textwrap.dedent("""
        import importlib.abc
        import sys

        class RejectOptionalImports(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname.split(".", 1)[0] in {"cv2", "numpy", "playwright"}:
                    raise AssertionError(
                        f"Unexpected optional import: {fullname}"
                    )

        finder = RejectOptionalImports()
        sys.meta_path.insert(0, finder)
        import majsoulrpa.screens.match as package

        for name in package.__all__:
            if name != "MatchScreen":
                assert getattr(package, name) is not None
        assert "majsoulrpa.screens.match.screen" not in sys.modules
        assert "majsoulrpa.presentation.template" not in sys.modules
        assert "majsoulrpa.assets.protocol.liqi_pb2" not in sys.modules

        sys.meta_path.remove(finder)
        from majsoulrpa.screens.match.screen import MatchScreen
        assert package.MatchScreen is MatchScreen
        assert package.__dict__["MatchScreen"] is MatchScreen
    """)

    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
