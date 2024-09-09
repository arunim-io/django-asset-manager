from pathlib import Path
import shutil
from typing import Literal

from pydantic import BaseModel, Field, computed_field

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


class PackageManagerSettings(BaseModel):
    name: Literal["npm", "yarn", "pnpm", "bun"] = Field(
        default="npm", description="The package manager to use.", alias="NAME"
    )

    @computed_field(
        description="""Path to the package manager.
        Must match with `PACKAGE_MANAGER.NAME`.
        """,
        alias="EXE_PATH",
    )
    @property
    def exe_path(self) -> Path | None:
        if exe := shutil.which(self.name):
            return Path(exe)
        return None

    class Config:
        from_attributes = True


class Settings(BaseModel):
    ignore_patterns: list[str] = Field(
        default=DEFAULT_IGNORE_PATTERNS,
        description="A list of patterns that will be ignored by the static finder.",
        alias="IGNORE_PATTERNS",
    )
    node_modules_path: Path = Field(
        default=Path(settings.BASE_DIR, "node_modules"),
        description="The path to `node_modules` directory.",
        alias="NODE_MODULES_PATH",
    )
    package_json_path: Path = Field(
        default=Path(settings.BASE_DIR, "package.json"),
        description="The path to `package.json`.",
        alias="PACKAGE_JSON_PATH",
    )
    package_manager: PackageManagerSettings = Field(
        ...,
        description="Options for package manager",
        alias="PACKAGE_MANAGER",
    )

    class Config:
        from_attributes = True


settings = Settings.model_validate(getattr(settings, "NODE_LOADER", {}))
