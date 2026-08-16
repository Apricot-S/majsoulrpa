import math
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytest
from pydantic import ValidationError

from majsoulrpa.presentation import (
    Region,
    TemplateMatcher,
    TemplateMatchResult,
    TemplateMatchSettings,
    load_png_template_matcher,
)


def _valid_settings_data() -> dict[str, Any]:
    return {
        "region": {
            "left": 100,
            "top": 200,
            "width": 320,
            "height": 80,
        },
        "margin": {"top": 4, "right": 5, "bottom": 6, "left": 7},
        "match": {"threshold": 0.92},
    }


def _make_small_template_matcher() -> TemplateMatcher:
    settings = TemplateMatchSettings.model_validate(
        {
            "region": {"left": 100, "top": 200, "width": 4, "height": 3},
            "margin": {"top": 0, "right": 0, "bottom": 0, "left": 0},
            "match": {"threshold": 0.99},
        },
    )
    return TemplateMatcher(np.zeros((3, 4), dtype=np.uint8), settings)


def test_template_match_settings_loads_from_toml_text() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 320
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
    )

    assert settings.region.left == 100
    assert settings.region.top == 200
    assert settings.region.width == 320
    assert settings.region.height == 80
    assert settings.margin.top == 4
    assert settings.margin.right == 5
    assert settings.margin.bottom == 6
    assert settings.margin.left == 7
    assert settings.match.threshold == 0.92


def test_template_match_settings_loads_from_toml_file(tmp_path: Path) -> None:
    settings_path = tmp_path / "template.toml"
    settings_path.write_text(
        """
        [region]
        left = 100
        top = 200
        width = 320
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
        encoding="utf-8",
    )

    settings = TemplateMatchSettings.from_toml_file(settings_path)

    assert settings.region.left == 100
    assert settings.region.top == 200
    assert settings.region.width == 320
    assert settings.region.height == 80
    assert settings.margin.top == 4
    assert settings.margin.right == 5
    assert settings.margin.bottom == 6
    assert settings.margin.left == 7
    assert settings.match.threshold == 0.92


def test_template_match_settings_rejects_unknown_key() -> None:
    with pytest.raises(ValidationError, match="extra"):
        TemplateMatchSettings.from_toml_text(
            """
            [region]
            left = 100
            top = 200
            width = 320
            height = 80
            unexpected = 1

            [margin]
            top = 4
            right = 5
            bottom = 6
            left = 7

            [match]
            threshold = 0.92
            """,
        )


@pytest.mark.parametrize(
    "toml_text",
    [
        """
        [region]
        left = -1
        top = 200
        width = 320
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
        """
        [region]
        left = 100
        top = 200
        width = 0
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
        """
        [region]
        left = 100
        top = 200
        width = 320
        height = 80

        [margin]
        top = -1
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
        """
        [region]
        left = 100
        top = 200
        width = 320
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 1.01
        """,
    ],
)
def test_template_match_settings_rejects_invalid_values(
    toml_text: str,
) -> None:
    with pytest.raises(ValidationError):
        TemplateMatchSettings.from_toml_text(toml_text)


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("region", "left"),
        ("region", "top"),
        ("region", "width"),
        ("region", "height"),
        ("margin", "top"),
        ("margin", "right"),
        ("margin", "bottom"),
        ("margin", "left"),
        ("match", "threshold"),
    ],
)
@pytest.mark.parametrize("value", ["1", True])
def test_template_match_settings_rejects_numeric_coercion(
    section: str,
    field: str,
    value: object,
) -> None:
    data = _valid_settings_data()
    data[section][field] = value

    with pytest.raises(ValidationError):
        TemplateMatchSettings.model_validate(data)


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("region", "left"),
        ("region", "top"),
        ("region", "width"),
        ("region", "height"),
        ("margin", "top"),
        ("margin", "right"),
        ("margin", "bottom"),
        ("margin", "left"),
        ("match", "threshold"),
    ],
)
@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_template_match_settings_rejects_non_finite_number(
    section: str,
    field: str,
    value: float,
) -> None:
    data = _valid_settings_data()
    data[section][field] = value

    with pytest.raises(ValidationError):
        TemplateMatchSettings.model_validate(data)


def test_region_config_converts_to_immutable_region() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 320
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
    )

    region = settings.region.to_region()

    assert region == Region(left=100, top=200, width=320, height=80)
    attr_name = "left"
    with pytest.raises(FrozenInstanceError):
        setattr(region, attr_name, 101)


def test_template_matcher_rejects_template_size_mismatch() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 320
        height = 80

        [margin]
        top = 4
        right = 5
        bottom = 6
        left = 7

        [match]
        threshold = 0.92
        """,
    )
    template = np.zeros((79, 320), dtype=np.uint8)

    with pytest.raises(ValueError, match="template size"):
        TemplateMatcher(template, settings)


@pytest.mark.parametrize(
    "template",
    [
        np.zeros(4, dtype=np.uint8),
        np.zeros((3, 4, 1), dtype=np.uint8),
    ],
)
def test_template_matcher_rejects_non_grayscale_template(
    template: np.ndarray,
) -> None:
    settings = TemplateMatchSettings.model_validate(
        {
            "region": {"left": 100, "top": 200, "width": 4, "height": 3},
            "margin": {"top": 0, "right": 0, "bottom": 0, "left": 0},
            "match": {"threshold": 0.99},
        },
    )

    with pytest.raises(ValueError, match="template must be a 2D"):
        TemplateMatcher(template, settings)


def test_template_matcher_rejects_non_uint8_template() -> None:
    settings = TemplateMatchSettings.model_validate(
        {
            "region": {"left": 100, "top": 200, "width": 4, "height": 3},
            "margin": {"top": 0, "right": 0, "bottom": 0, "left": 0},
            "match": {"threshold": 0.99},
        },
    )

    with pytest.raises(TypeError, match="template dtype must be uint8"):
        TemplateMatcher(np.zeros((3, 4), dtype=np.float32), settings)


@pytest.mark.parametrize(
    "shape",
    [
        (0, 4),
        (3, 0),
    ],
)
def test_template_matcher_rejects_empty_template(
    shape: tuple[int, int],
) -> None:
    settings = TemplateMatchSettings.model_validate(
        {
            "region": {"left": 100, "top": 200, "width": 4, "height": 3},
            "margin": {"top": 0, "right": 0, "bottom": 0, "left": 0},
            "match": {"threshold": 0.99},
        },
    )

    with pytest.raises(ValueError, match="template must not be empty"):
        TemplateMatcher(np.zeros(shape, dtype=np.uint8), settings)


@pytest.mark.parametrize(
    "screenshot",
    [
        np.zeros(1920, dtype=np.uint8),
        np.zeros((1080, 1920, 1), dtype=np.uint8),
    ],
)
def test_template_matcher_rejects_non_grayscale_screenshot(
    screenshot: np.ndarray,
) -> None:
    matcher = _make_small_template_matcher()

    with pytest.raises(ValueError, match="screenshot must be a 2D"):
        matcher.match(screenshot)


def test_template_matcher_rejects_non_uint8_screenshot() -> None:
    matcher = _make_small_template_matcher()

    with pytest.raises(TypeError, match="screenshot dtype must be uint8"):
        matcher.match(np.zeros((1080, 1920), dtype=np.float32))


@pytest.mark.parametrize(
    "shape",
    [
        (0, 1920),
        (1080, 0),
    ],
)
def test_template_matcher_rejects_empty_screenshot(
    shape: tuple[int, int],
) -> None:
    matcher = _make_small_template_matcher()

    with pytest.raises(ValueError, match="screenshot must not be empty"):
        matcher.match(np.zeros(shape, dtype=np.uint8))


def test_template_matcher_uses_scale_one_for_1920x1080_screenshot() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 4
        height = 3

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 64, 128, 255],
            [255, 128, 64, 0],
            [32, 96, 160, 224],
        ],
        dtype=np.uint8,
    )
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    screenshot[200:203, 100:104] = template

    matcher = TemplateMatcher(template, settings)
    result = matcher.match(screenshot)

    assert result == TemplateMatchResult(
        score=1.0,
        region=Region(left=100, top=200, width=4, height=3),
    )
    assert matcher.find(screenshot) == result
    assert matcher.matches(screenshot) is True


def test_template_matcher_scales_to_1280x720_screenshot() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 300
        top = 150
        width = 6
        height = 3

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 32, 64, 96, 128, 160],
            [160, 128, 96, 64, 32, 0],
            [16, 48, 80, 112, 144, 176],
        ],
        dtype=np.uint8,
    )
    scaled_template = cv2.resize(
        template,
        (4, 2),
        interpolation=cv2.INTER_LINEAR,
    )
    screenshot = np.zeros((720, 1280), dtype=np.uint8)
    screenshot[100:102, 200:204] = scaled_template

    matcher = TemplateMatcher(template, settings)
    result = matcher.match(screenshot)

    assert result.region == Region(left=200, top=100, width=4, height=2)
    assert result.score == pytest.approx(1.0)
    assert matcher.matches(screenshot) is True


def test_template_matcher_scales_to_2560x1440_screenshot() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 300
        top = 150
        width = 6
        height = 3

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 32, 64, 96, 128, 160],
            [160, 128, 96, 64, 32, 0],
            [16, 48, 80, 112, 144, 176],
        ],
        dtype=np.uint8,
    )
    scaled_template = cv2.resize(
        template,
        (8, 4),
        interpolation=cv2.INTER_LINEAR,
    )
    screenshot = np.zeros((1440, 2560), dtype=np.uint8)
    screenshot[200:204, 400:408] = scaled_template

    matcher = TemplateMatcher(template, settings)
    result = matcher.match(screenshot)

    assert result.region == Region(left=400, top=200, width=8, height=4)
    assert result.score == pytest.approx(1.0)
    assert matcher.matches(screenshot) is True


def test_template_matcher_rejects_non_16_to_9_screenshot() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 4
        height = 3

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 64, 128, 255],
            [255, 128, 64, 0],
            [32, 96, 160, 224],
        ],
        dtype=np.uint8,
    )
    screenshot = np.zeros((1000, 1000), dtype=np.uint8)
    matcher = TemplateMatcher(template, settings)

    with pytest.raises(ValueError, match="16:9"):
        matcher.match(screenshot)


def test_template_matcher_finds_template_shifted_within_margin() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 4
        height = 3

        [margin]
        top = 8
        right = 9
        bottom = 10
        left = 11

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 64, 128, 255],
            [255, 128, 64, 0],
            [32, 96, 160, 224],
        ],
        dtype=np.uint8,
    )
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    screenshot[195:198, 107:111] = template

    matcher = TemplateMatcher(template, settings)
    result = matcher.match(screenshot)

    assert result.region == Region(left=107, top=195, width=4, height=3)
    assert result.score == pytest.approx(1.0)


def test_template_matcher_uses_better_score_between_ccoeff_and_sqdiff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 4
        height = 3

        [margin]
        top = 0
        right = 4
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 64, 128, 255],
            [255, 128, 64, 0],
            [32, 96, 160, 224],
        ],
        dtype=np.uint8,
    )
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)

    def fake_match_template(
        image: np.ndarray,
        templ: np.ndarray,
        method: int,
    ) -> np.ndarray:
        assert image.shape == (3, 8)
        assert templ.shape == (3, 4)
        if method == cv2.TM_CCOEFF_NORMED:
            return np.array([[0.2, 0.4, 0.7, 0.3, 0.1]], dtype=np.float32)
        if method == cv2.TM_SQDIFF_NORMED:
            return np.array([[0.8, 0.6, 0.5, 0.04, 0.7]], dtype=np.float32)
        raise AssertionError

    monkeypatch.setattr(cv2, "matchTemplate", fake_match_template)

    matcher = TemplateMatcher(template, settings)
    result = matcher.match(screenshot)

    assert result.region == Region(left=103, top=200, width=4, height=3)
    assert result.score == pytest.approx(0.96)


@pytest.mark.parametrize(
    "score",
    [math.nan, math.inf, -math.inf, -0.01, 1.01],
)
def test_template_match_result_rejects_invalid_score(score: float) -> None:
    with pytest.raises(ValueError, match="score"):
        TemplateMatchResult(
            score=score,
            region=Region(left=100, top=200, width=4, height=3),
        )


def test_template_matcher_rejects_non_finite_opencv_score(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    matcher = _make_small_template_matcher()
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)

    def fake_match_template(
        image: np.ndarray,
        templ: np.ndarray,
        method: int,
    ) -> np.ndarray:
        _ = image, templ, method
        return np.array([[math.nan]], dtype=np.float32)

    monkeypatch.setattr(cv2, "matchTemplate", fake_match_template)

    with pytest.raises(ValueError, match="score"):
        matcher.matches(screenshot)


def test_template_matcher_returns_false_below_threshold() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 100
        top = 200
        width = 4
        height = 3

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 64, 128, 255],
            [255, 128, 64, 0],
            [32, 96, 160, 224],
        ],
        dtype=np.uint8,
    )
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)

    matcher = TemplateMatcher(template, settings)

    assert matcher.find(screenshot) is None
    assert matcher.matches(screenshot) is False


def test_template_matcher_rejects_too_small_search_area() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 1900
        top = 1000
        width = 4
        height = 3

        [margin]
        top = 0
        right = 100
        bottom = 100
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.array(
        [
            [0, 64, 128, 255],
            [255, 128, 64, 0],
            [32, 96, 160, 224],
        ],
        dtype=np.uint8,
    )
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    matcher = TemplateMatcher(template, settings)

    with pytest.raises(ValueError, match="search region"):
        matcher.match(screenshot)


def test_template_matcher_rejects_too_small_scaled_template() -> None:
    settings = TemplateMatchSettings.from_toml_text(
        """
        [region]
        left = 0
        top = 0
        width = 0.6
        height = 3

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
    )
    template = np.zeros((3, 1), dtype=np.uint8)
    screenshot = np.zeros((720, 1280), dtype=np.uint8)
    matcher = TemplateMatcher(template, settings)

    with pytest.raises(ValueError, match="scaled region size"):
        matcher.match(screenshot)


def test_load_png_template_matcher_from_files(tmp_path: Path) -> None:
    template = np.array(
        [
            [0, 64],
            [128, 255],
        ],
        dtype=np.uint8,
    )
    template_path = tmp_path / "template.png"
    settings_path = tmp_path / "template.toml"
    assert cv2.imwrite(str(template_path), template)
    settings_path.write_text(
        """
        [region]
        left = 100
        top = 200
        width = 2
        height = 2

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
        encoding="utf-8",
    )
    screenshot = np.zeros((1080, 1920), dtype=np.uint8)
    screenshot[200:202, 100:102] = template
    success, screenshot_png = cv2.imencode(".png", screenshot)
    assert success

    matcher = load_png_template_matcher(
        template_path=template_path,
        settings_path=settings_path,
    )

    assert matcher.matches(screenshot_png.tobytes()) is True
    assert matcher.find(screenshot_png.tobytes()) == TemplateMatchResult(
        score=1.0,
        region=Region(left=100, top=200, width=2, height=2),
    )
    assert matcher.match(screenshot_png.tobytes()).region == Region(
        left=100,
        top=200,
        width=2,
        height=2,
    )


def test_load_png_template_matcher_rejects_invalid_png(tmp_path: Path) -> None:
    template_path = tmp_path / "template.png"
    settings_path = tmp_path / "template.toml"
    template_path.write_bytes(b"not png")
    settings_path.write_text(
        """
        [region]
        left = 100
        top = 200
        width = 2
        height = 2

        [margin]
        top = 0
        right = 0
        bottom = 0
        left = 0

        [match]
        threshold = 0.99
        """,
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="PNG image"):
        load_png_template_matcher(
            template_path=template_path,
            settings_path=settings_path,
        )
