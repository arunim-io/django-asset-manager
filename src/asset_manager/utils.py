from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .staticfiles.finders import NodeModulesFinder


def get_staticfiles_finder() -> NodeModulesFinder:
    staticfiles_finders = getattr(django_settings, "STATICFILES_FINDERS", None)  # pyright: ignore[reportAttributeAccessIssue]

    if not staticfiles_finders:
        msg = "`STATICFILES_FINDERS` must not be empty."
        raise ImproperlyConfigured(msg)

    if "asset_manager.staticfiles.finders.NodeModulesFinder" in staticfiles_finders:
        finder_path = "asset_manager.staticfiles.finders.NodeModulesFinder"
    if (
        "asset_manager.staticfiles.finders.ManifestNodeModulesFinder"
        in staticfiles_finders
    ):
        finder_path = "asset_manager.staticfiles.finders.ManifestNodeModulesFinder"

    return import_string(finder_path) if finder_path else None
