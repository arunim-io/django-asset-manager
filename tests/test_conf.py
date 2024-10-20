import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pytest_mock import MockerFixture

from django.conf import LazySettings

from asset_manager.conf import Settings


@pytest.fixture(autouse=True)
def app_settings(settings):
    settings.ASSET_MANAGER = {}
    return Settings.parse(**settings.ASSET_MANAGER)


def test_settings_type(settings: LazySettings, app_settings: Settings):
    assert settings.ASSET_MANAGER == {}
    assert type(app_settings) == Settings


@pytest.fixture
def temp_dir():
    tmpdir = TemporaryDirectory()

    yield tmpdir.name

    tmpdir.cleanup()


def test_settings_package_dependencies(app_settings: Settings, temp_dir: str):
    assert app_settings.package_dependencies is None

    tmp_package_json = Path(temp_dir, "package.json")
    tmp_package_json.write_text(json.dumps({"dependencies": {}}))
    app_settings.package_json_path = tmp_package_json

    assert app_settings.package_dependencies == {}


def test_package_manager_settings_exe_path(
    app_settings: Settings,
    mocker: MockerFixture,
):
    assert app_settings.package_manager.exe_path is None

    mocker.patch("shutil.which", return_value="/usr/bin/git")
    assert app_settings.package_manager.exe_path is not None
