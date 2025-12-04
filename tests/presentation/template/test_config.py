from pathlib import Path

import pytest

from majsoulrpa.presentation.template.config import Config


def write_toml(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_from_file_boundary_values(tmp_path: Path) -> None:
    toml_content = """
    [region]
    left = 0
    top = 0
    width = 1
    height = 1

    [margin]
    left = 0
    right = 0
    top = 0
    bottom = 0

    [settings]
    threshold = 0.0000001
    """
    config_file = tmp_path / "config_boundary.toml"
    write_toml(config_file, toml_content)

    cfg = Config.from_file(config_file)

    assert cfg.region.left == 0
    assert cfg.region.width == 1
    assert cfg.margin.bottom == 0
    assert cfg.settings.threshold > 0.0


def test_from_file_normal_values(tmp_path: Path) -> None:
    toml_content = """
    [region]
    left = 100
    top = 200
    width = 300
    height = 400

    [margin]
    left = 10
    right = 20
    top = 5
    bottom = 15

    [settings]
    threshold = 0.75
    """
    config_file = tmp_path / "config_normal.toml"
    write_toml(config_file, toml_content)

    cfg = Config.from_file(config_file)

    assert cfg.region.left == 100
    assert cfg.region.height == 400
    assert cfg.margin.right == 20
    assert pytest.approx(cfg.settings.threshold, rel=1e-9) == 0.75
