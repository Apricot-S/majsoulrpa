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


def test_get_image_success(tmp_image: Path) -> None:
    fi = FileImage(tmp_image)
    image = fi.get_image()
    assert (image.shape[1], image.shape[0]) == (200, 100)


def test_get_image_file_not_found(tmp_path: Path) -> None:
    path = tmp_path / "not_exist.png"
    fi = FileImage(path)
    with pytest.raises(ImageLoadError):
        fi.get_image()


def test_get_image_cache(tmp_image: Path) -> None:
    fi = FileImage(tmp_image)

    with patch.object(FileImage, "_load", wraps=fi._load) as mock_load:
        fi.get_image()
        assert mock_load.call_count == 1

        fi.get_image()
        assert mock_load.call_count == 1
