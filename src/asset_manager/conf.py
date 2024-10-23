import json
from pathlib import Path
from typing import TypedDict

from django.conf import settings as django_settings

DEFAULT_IGNORE_PATTERNS = [
    "*.less",
    "*.scss",
    "*.styl",
    "*.sh",
    "*.htm",
    "*.html",
    "*.md",
    "*.markdown",
    "*.rst",
    "*.php",
    "*.rb",
    "*.txt",
    "*.map",
    "*.yml",
    "*.yaml",
    "*.json",
    "*.xml",
    "*.ts",
    "*.es6",
    "*.coffee",
    "*.litcoffee",
    "*.lock",
    "*.patch",
    "README*",
    "LICENSE*",
    "LICENCE*",
    "CHANGES",
    "CHANGELOG",
    "HISTORY",
    "NOTICE",
    "COPYING",
    "license",
    "*test*",
    "*bin*",
    "*samples*",
    "*example*",
    "*docs*",
    "*tests*",
    "*demo*",
    "Makefile*",
    "Gemfile*",
    "Gruntfile*",
    "gulpfile.js",
    ".tagconfig",
    ".npmignore",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".editorconfig",
    ".sqlite",
    "grunt",
    "gulp",
    "less",
    "sass",
    "scss",
    "coffee",
    "tasks",
    "node_modules",
]
DEFAULT_NODE_MODULES_PATH = Path(django_settings.BASE_DIR, "node_modules")
DEFAULT_PACKAGE_JSON_PATH = Path(django_settings.BASE_DIR, "package.json")


class SettingsDict(TypedDict):
    IGNORE_PATTERNS: list[str]
    NODE_MODULES_PATH: Path | None
    PACKAGE_JSON_PATH: Path | None


def settings() -> SettingsDict:
    app_settings = getattr(django_settings, "ASSET_MANAGER", {})

    if "IGNORE_PATTERNS" not in app_settings:
        app_settings["IGNORE_PATTERNS"] = DEFAULT_IGNORE_PATTERNS

    if "NODE_MODULES_PATH" not in app_settings and DEFAULT_NODE_MODULES_PATH.exists():
        app_settings["NODE_MODULES_PATH"] = DEFAULT_NODE_MODULES_PATH
    if isinstance(app_settings.get("NODE_MODULES_PATH"), str):
        app_settings["NODE_MODULES_PATH"] = Path(app_settings["NODE_MODULES_PATH"])

    if "PACKAGE_JSON_PATH" not in app_settings and DEFAULT_PACKAGE_JSON_PATH.exists():
        app_settings["PACKAGE_JSON_PATH"] = DEFAULT_PACKAGE_JSON_PATH
    if isinstance(app_settings.get("PACKAGE_JSON_PATH"), str):
        app_settings["PACKAGE_JSON_PATH"] = Path(app_settings["PACKAGE_JSON_PATH"])

    return SettingsDict(**app_settings)


def get_package_dependencies(path=None) -> dict[str, str] | None:
    package_json_path = (
        Path(path) if path is not None else settings().get("PACKAGE_JSON_PATH")
    )

    if not package_json_path or not package_json_path.exists():
        return None
    with package_json_path.open() as f:
        data = json.load(f)

    return data.get("dependencies")
