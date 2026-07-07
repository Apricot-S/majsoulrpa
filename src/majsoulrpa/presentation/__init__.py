import importlib
from typing import TYPE_CHECKING, Any

from majsoulrpa.presentation.region import Region

_TEMPLATE_EXPORTS = {
    "load_png_template_matcher",
    "PngTemplateMatcher",
    "TemplateMatcher",
    "TemplateMatchResult",
    "TemplateMatchSettings",
}

if TYPE_CHECKING:
    from majsoulrpa.presentation.template import (
        PngTemplateMatcher,
        TemplateMatcher,
        TemplateMatchResult,
        TemplateMatchSettings,
        load_png_template_matcher,
    )

__all__ = [
    "PngTemplateMatcher",
    "Region",
    "TemplateMatchResult",
    "TemplateMatchSettings",
    "TemplateMatcher",
    "load_png_template_matcher",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    if name in _TEMPLATE_EXPORTS:
        try:
            template = importlib.import_module(
                "majsoulrpa.presentation.template",
            )
        except ModuleNotFoundError as error:
            msg = (
                f"{name} requires the 'rpa' optional dependency. "
                "Install it with: pip install 'majsoulrpa[rpa]'"
            )
            raise ModuleNotFoundError(msg) from error

        value = getattr(template, name)
        globals()[name] = value
        return value

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> list[str]:
    return sorted({*globals(), *__all__})
