from abc import ABC, abstractmethod
from pathlib import Path
from typing import override

import cv2


class ImageBase(ABC):
    @abstractmethod
    def get_scaled(self, scale: float) -> cv2.typing.MatLike:
        pass


class ImageLoadError(Exception):
    """Raised when an image cannot be loaded from the given source."""


class FileImage(ImageBase):
    def __init__(self, path: Path) -> None:
        self._path = path
        self._original: cv2.typing.MatLike | None = None

    def _load(self) -> cv2.typing.MatLike:
        image = cv2.imread(str(self._path), cv2.IMREAD_COLOR)
        if image is None:
            msg = f"failed to load image: {self._path}"
            raise ImageLoadError(msg)
        return image

    @override
    def get_scaled(self, scale: float) -> cv2.typing.MatLike:
        if self._original is None:
            self._original = self._load()
        return cv2.resize(self._original, None, fx=scale, fy=scale)
