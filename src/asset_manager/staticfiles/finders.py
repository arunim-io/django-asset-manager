# ruff: noqa: E501

from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.utils import get_files
from django.core.files.storage import FileSystemStorage

from asset_manager.conf import get_package_dependencies, settings


class NodeModulesFinder(BaseFinder):
    """
    A static files finder that finds static files stored in the `node_modules` directory (specified in the `NODE_MODULES_PATH` settings), while excluding any metadata or misc. files.
    """

    storage = FileSystemStorage(location=str(settings().get("NODE_MODULES_PATH")))

    def find(self, path: str, *args, **kwargs) -> str | list[str]:
        paths = []

        if self.storage.exists(path):
            path = self.storage.path(path)

            if not kwargs.get("find_all", False):
                return path

            paths.append(path)

        return paths

    def list(self, ignore_patterns):
        if not ignore_patterns:
            ignore_patterns = settings.get("IGNORE_PATTERNS")

        for path in get_files(self.storage, ignore_patterns):
            yield path, self.storage


class ManifestNodeModulesFinder(NodeModulesFinder):
    """
    A static files finder that is the same as `NodeModulesFinder` but finds static files in the directories of the dependencies that are specified in `package.json`.
    """

    def list(self, ignore_patterns):
        if not ignore_patterns:
            ignore_patterns = settings.get("IGNORE_PATTERNS")

        deps = get_package_dependencies()

        if not deps:
            yield from self.list(ignore_patterns)

        for package in deps:
            if self.storage.exists(package):
                for path in get_files(self.storage, ignore_patterns, package):
                    yield path, self.storage
