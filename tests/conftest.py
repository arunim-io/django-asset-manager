from pathlib import Path

import pytest

from django.conf import (
    LazySettings,
    settings as django_settings,
)


def pytest_configure():
    django_settings.configure(
        DEBUG=True,
        SECRET_KEY="NOTASECRET",
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=["django.contrib.staticfiles", "asset_manager"],
        USE_TZ=True,
        STATIC_URL="/static/",
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
            "asset_manager.staticfiles.finders.ManifestNodeModulesFinder",
        ],
        BASE_DIR=Path(__name__).parent,
    )


@pytest.fixture(autouse=True)
def setup_base_dir(settings: LazySettings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
