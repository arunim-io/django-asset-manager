import json
from pathlib import Path
from typing import TypedDict

from django.conf import settings as django_settings


class SettingsDict(TypedDict, total=False):
    IGNORE_PATTERNS: list[str]
    NODE_MODULES_PATH: Path | str
    PACKAGE_JSON_PATH: Path | str


DEFAULT_SETTINGS: SettingsDict = {
    "DEFAULT_IGNORE_PATTERNS": [
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
    ],
    "DEFAULT_NODE_MODULES_PATH": Path(django_settings.BASE_DIR, "node_modules"),
    "DEFAULT_PACKAGE_JSON_PATH": Path(django_settings.BASE_DIR, "package.json"),
}


def settings() -> SettingsDict:
    app_settings: SettingsDict = getattr(
        django_settings,
        "ASSET_MANAGER",
        DEFAULT_SETTINGS,
    )

    if isinstance(app_settings.get("NODE_MODULES_PATH"), str):
        app_settings["NODE_MODULES_PATH"] = Path(app_settings["NODE_MODULES_PATH"])

    if isinstance(app_settings.get("PACKAGE_JSON_PATH"), str):
        app_settings["PACKAGE_JSON_PATH"] = Path(app_settings["PACKAGE_JSON_PATH"])

    return app_settings


def get_package_dependencies(path=None) -> dict[str, str] | None:
    package_json_path = (
        Path(path) if path is not None else settings().get("PACKAGE_JSON_PATH")
    )

    if not package_json_path or not package_json_path.exists():
        return None
    with package_json_path.open() as f:
        data = json.load(f)

    return data.get("dependencies")
