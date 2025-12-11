from abc import ABC, abstractmethod
from pathlib import Path
from typing import override

import cv2
from cv2.typing import MatLike


class ImageBase[T](ABC):
    @abstractmethod
    def get_image(self) -> T:
        pass


class ImageLoadError(Exception):
    """Raised when an image cannot be loaded from the given source."""


class FileImage(ImageBase[MatLike]):
    def __init__(self, path: Path) -> None:
        self._path = path
        self._image: MatLike | None = None

    def _load(self) -> MatLike:
        image = cv2.imread(str(self._path), cv2.IMREAD_COLOR)
        if image is None:
            msg = f"failed to load image: {self._path}"
            raise ImageLoadError(msg)
        return image

    @override
    def get_image(self) -> MatLike:
        if self._image is None:
            self._image = self._load()
        return self._image
