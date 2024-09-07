from pathlib import Path

from pydantic import BaseModel, Field

from django.conf import settings

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


class Settings(BaseModel):
    IGNORE_PATTERNS: list[str] = Field(
        default=DEFAULT_IGNORE_PATTERNS,
        description="A list of patterns that will be ignored by the static finder.",
    )
    NODE_MODULES_PATH: Path = Field(
        default=Path(settings.BASE_DIR, "node_modules"),
        description="The path to `node_modules` directory.",
    )
    PACKAGE_JSON_PATH: Path = Field(
        default=Path(settings.BASE_DIR, "package.json"),
        description="The path to `package.json`.",
    )

    class Config:
        from_attributes = True


settings = Settings.model_validate(getattr(settings, "NODE_LOADER", {}))
