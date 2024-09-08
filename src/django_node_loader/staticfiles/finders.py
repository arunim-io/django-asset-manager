# ruff: noqa: E501

import json

from django_node_loader.conf import settings

from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.utils import get_files
from django.core.files.storage import FileSystemStorage


class NodeModulesFinder(BaseFinder):
    """
    A static files finder that finds static files stored in the `node_modules` directory (specified in the `NODE_MODULES_PATH` settings), while excluding any metadata or misc. files.
    """

    storage = FileSystemStorage(location=settings.NODE_MODULES_PATH)

    def find(self, path: str, *args, **kwargs) -> str | list[str]:
        paths = []

        if self.storage.exists(path):
            path = self.storage.path(path)

            if not kwargs.get("find_all", False):
                return path

            paths.append(path)

        return paths

    def list(self, ignore_patterns):
        for path in get_files(self.storage, settings.IGNORE_PATTERNS):
            yield path, self.storage


class ManifestNodeModulesFinder(NodeModulesFinder):
    """
    A static files finder that is the same as `NodeModulesFinder` but finds static files in the directories of the dependencies that are specified in `package.json`.
    """

    def list(self, ignore_patterns):
        try:
            package_json = json.loads(settings.PACKAGE_JSON_PATH.read_bytes())
        except json.JSONDecodeError:
            yield from self.list(ignore_patterns)

        if package_json["dependencies"] is dict:
            packages = dict(package_json["dependencies"]).keys()

            for package in packages:
                if self.storage.exists(package):
                    for path in get_files(
                        self.storage, settings.IGNORE_PATTERNS, package
                    ):
                        yield path, self.storage
