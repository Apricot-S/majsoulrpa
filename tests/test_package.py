import majsoulrpa


def test_package_exposes_version() -> None:
    assert majsoulrpa.__version__ == "0.1.0"


def test_public_exports_are_explicit() -> None:
    assert majsoulrpa.__all__ == ["AppConfig", "__version__"]
