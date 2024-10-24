import json

from pytest_mock import MockFixture

from django.conf import LazySettings

from asset_manager.conf import (
    DEFAULT_IGNORE_PATTERNS,
    get_package_dependencies,
    settings as app_settings,
)


def test_parse_settings_default(settings: LazySettings):
    settings.ASSET_MANAGER = {}

    parsed_settings = app_settings()

    assert parsed_settings.get("IGNORE_PATTERNS") == DEFAULT_IGNORE_PATTERNS
    assert parsed_settings.get("NODE_MODULES_PATH") is None
    assert parsed_settings.get("PACKAGE_JSON_PATH") is None


def test_parse_settings_custom(settings: LazySettings):
    settings.ASSET_MANAGER = {
        "IGNORE_PATTERNS": ["*.txt"],
        "NODE_MODULES_PATH": "/custom/node_modules",
        "PACKAGE_JSON_PATH": "/custom/package.json",
    }

    parsed_settings = app_settings()

    assert parsed_settings


def test_get_package_dependencies(
    settings: LazySettings,
    mocker: MockFixture,
    tmp_path,
):
    package_json = tmp_path / "package.json"
    content = {"dependencies": {"htmx.org": "latest"}}

    with package_json.open("w") as f:
        f.write(json.dumps(content))

    settings.ASSET_MANAGER = {"PACKAGE_JSON_PATH": package_json}

    mock_open = mocker.mock_open(read_data=json.dumps(content))
    mocker.patch("pathlib.Path.open", mock_open)
    mocker.patch("pathlib.Path.exists", return_value=True)

    dependencies = get_package_dependencies()

    assert dependencies is not None
    assert dependencies == content["dependencies"]


def test_get_package_dependencies_no_file(settings: LazySettings):
    settings.ASSET_MANAGER = {"PACKAGE_JSON_PATH": None}

    dependencies = get_package_dependencies()

    assert dependencies is None
