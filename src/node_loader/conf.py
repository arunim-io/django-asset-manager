from dataclasses import dataclass, field, fields
from pathlib import Path
import shutil
from typing import Literal

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


@dataclass
class PackageManagerSettings:
    name: Literal["npm", "yarn", "pnpm", "bun"] = "npm"

    @property
    def exe_path(self) -> Path | None:
        if exe := shutil.which(self.name):
            return Path(exe)
        return None


@dataclass
class Settings:
    ignore_patterns: list[str] = field(default_factory=lambda: DEFAULT_IGNORE_PATTERNS)
    node_modules_path: Path = Path(settings.BASE_DIR, "node_modules")
    package_json_path: Path = Path(settings.BASE_DIR, "package.json")
    package_manager: PackageManagerSettings = field(
        default_factory=PackageManagerSettings,
    )

    @staticmethod
    def parse():
        parsed_settings = {
            field.name: getattr(settings, field.name.upper(), field.default)
            for field in fields(Settings)
        }
        return Settings(**parsed_settings)  # pyright: ignore[reportArgumentType]


settings = Settings.parse()
