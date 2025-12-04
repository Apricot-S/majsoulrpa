from pathlib import Path
from unittest.mock import patch

import cv2
import numpy as np
import pytest

from majsoulrpa.presentation.template.image import FileImage, ImageLoadError


@pytest.fixture
def tmp_image(tmp_path: Path) -> Path:
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    path = tmp_path / "test.png"
    cv2.imwrite(str(path), img)
    return path


@pytest.mark.parametrize(
    ("scale", "width", "height"),
    [(1.0, 200, 100), (0.5, 100, 50), (2.0, 400, 200)],
)
def test_get_scaled_success(
    tmp_image: Path,
    scale: float,
    width: int,
    height: int,
) -> None:
    fi = FileImage(tmp_image)
    scaled = fi.get_scaled(scale)
    assert (scaled.shape[1], scaled.shape[0]) == (width, height)


def test_get_scaled_file_not_found(tmp_path: Path) -> None:
    path = tmp_path / "not_exist.png"
    fi = FileImage(path)
    with pytest.raises(ImageLoadError):
        fi.get_scaled(1.0)


def test_get_scaled_cache(tmp_image: Path) -> None:
    fi = FileImage(tmp_image)

    with patch.object(FileImage, "_load", wraps=fi._load) as mock_load:
        fi.get_scaled(1.0)
        assert mock_load.call_count == 1

        fi.get_scaled(2.0)
        assert mock_load.call_count == 1
