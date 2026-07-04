from majsoulrpa.cli import main


def test_browser_cli_entry_point_accepts_empty_arguments() -> None:
    assert main([]) == 0
