from pathlib import Path

import pytest

from django.conf import settings


def pytest_configure():
    settings.configure(
        DEBUG=True,
        SECRET_KEY="NOTASECRET",
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=["asset_manager"],
        USE_TZ=True,
        STATIC_URL="/static/",
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
            "asset_manager.staticfiles.finders.ManifestNodeModulesFinder",
        ],
    )


@pytest.fixture(scope="session")
def setup_base_dir(tmp_path: Path):
    settings.BASE_DIR = tmp_path
