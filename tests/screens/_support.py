import datetime
from importlib.resources.abc import Traversable
from typing import Any

import cv2
import numpy as np
from pydantic import JsonValue

from majsoulrpa.presentation.template import TemplateMatchSettings
from majsoulrpa.screens import ScreenContext as FrameworkScreenContext
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
    Direction,
    RawNotice,
    RawRequestResponse,
)
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from tests.sniffer.fakes import EMPTY_SNIFFER_MESSAGES


def ScreenContext(**kwargs: Any) -> FrameworkScreenContext:  # noqa: N802, ANN401
    kwargs.setdefault("sniffer_messages", EMPTY_SNIFFER_MESSAGES)
    return FrameworkScreenContext(**kwargs)


class BrowserControllerSpy:
    def __init__(self, screenshot: bytes, *screenshots: bytes) -> None:
        self.clicked_points: list[tuple[float, float]] = []
        self.moved_points: list[tuple[float, float]] = []
        self.screenshot_bytes = screenshot
        self.screenshot_queue = [screenshot, *screenshots]
        self.screenshot_count = 0
        self.events: list[str] = []

    async def click(self, x: float, y: float, *, warp: bool = False) -> None:
        _ = warp
        self.clicked_points.append((x, y))

    async def move_mouse(self, x: float, y: float) -> None:
        self.moved_points.append((x, y))
        self.events.append("move_mouse")

    async def goto_url(self, url: str) -> None:
        _ = url

    async def reload(self) -> None:
        pass

    async def stop_browser_host(self) -> None:
        pass

    async def click_and_wait_for_yostar_auth(
        self,
        x: float,
        y: float,
    ) -> object:
        _ = (x, y)
        return object()

    async def input_text(self, text: str) -> None:
        _ = text

    async def press_key(self, key: str) -> None:
        _ = key

    async def screenshot(self) -> bytes:
        self.events.append("screenshot")
        self.screenshot_count += 1
        if self.screenshot_queue:
            return self.screenshot_queue.pop(0)
        return self.screenshot_bytes


def _synthetic_template_screenshot(
    *,
    template_path: Traversable,
    settings_path: Traversable,
) -> bytes:
    return _synthetic_templates_screenshot(
        ((template_path, settings_path),),
    )


def _synthetic_templates_screenshot(
    assets: tuple[tuple[Traversable, Traversable], ...],
) -> bytes:
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    for template_path, settings_path in assets:
        encoded = np.frombuffer(template_path.read_bytes(), dtype=np.uint8)
        template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
        assert template is not None
        settings = TemplateMatchSettings.from_toml_file(settings_path)
        region = settings.region
        left = round(region.left)
        top = round(region.top)
        width = round(region.width)
        height = round(region.height)
        screenshot[top : top + height, left : left + width] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def _synthetic_blank_screenshot() -> bytes:
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def _synthetic_template_at_screenshot(
    *,
    template_path: Traversable,
    left: int,
    top: int,
) -> bytes:
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    encoded = np.frombuffer(template_path.read_bytes(), dtype=np.uint8)
    template = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    assert template is not None
    height, width = template.shape
    screenshot[top : top + height, left : left + width] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success
    return screenshot_png.tobytes()


def _notice(name: str) -> DecodedNotice:
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=name,
            payload=b"synthetic",
            observed_at=datetime.datetime(
                2026,
                1,
                2,
                tzinfo=datetime.UTC,
            ),
        ),
        message={},
    )


def _request_response(
    name: str,
    response: dict[str, JsonValue],
) -> DecodedRequestResponse:
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    return DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=name,
            request=b"synthetic-request",
            response=b"synthetic-response",
            request_observed_at=observed_at,
            response_observed_at=observed_at,
        ),
        request={},
        response=response,
    )


def _message_queue(
    *messages: str | DecodedSnifferMessage,
) -> SnifferMessageQueue:
    queue = SnifferMessageQueue(capacity=10, max_payload_bytes=1024)
    for message in messages:
        queue.enqueue(
            _notice(message) if isinstance(message, str) else message
        )
    return queue
