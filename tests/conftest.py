from pathlib import Path

from django.conf import settings as django_settings


def pytest_configure():
    django_settings.configure(
        DEBUG=True,
        SECRET_KEY="NOTASECRET",
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=["asset_manager"],
        USE_TZ=True,
        STATIC_URL="/static/",
        STATICFILES_FINDERS=[
            "asset_manager.staticfiles.finders.ManifestNodeModulesFinder"
        ],
        BASE_DIR=Path(__name__).parent,
    )
