from importlib.resources import files

ASSETS_DIR = files("majsoulrpa.assets")
TEMPLATES_DIR = ASSETS_DIR / "templates"

__all__ = ["ASSETS_DIR", "TEMPLATES_DIR"]
