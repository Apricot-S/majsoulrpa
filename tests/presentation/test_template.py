from dataclasses import FrozenInstanceError

import cv2
import numpy as np
import pytest
from pydantic import ValidationError

from majsoulrpa.presentation import (
    Region,
    TemplateMatcher,
    TemplateMatchResult,
    TemplateMatchSettings,
)


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


def test_region_calculates_right_and_bottom() -> None:
    region = Region(left=100, top=200, width=320, height=80)

    assert region.right == 420
    assert region.bottom == 280


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
        interpolation=cv2.INTER_AREA,
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
        interpolation=cv2.INTER_AREA,
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
        width = 0.1
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
    template = np.zeros((3, 0), dtype=np.uint8)
    screenshot = np.zeros((720, 1280), dtype=np.uint8)
    matcher = TemplateMatcher(template, settings)

    with pytest.raises(ValueError, match="scaled region size"):
        matcher.match(screenshot)
