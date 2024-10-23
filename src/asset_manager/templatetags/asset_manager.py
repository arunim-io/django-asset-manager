from pathlib import Path

from django.template import Library, TemplateSyntaxError
from django.templatetags.static import static

from asset_manager.conf import get_package_dependencies, settings
from asset_manager.utils import get_staticfiles_finder

register = Library()
finder = get_staticfiles_finder()
node_modules_path = settings().get("NODE_MODULES_PATH")


def resolve_path(path: str):
    subs = Path(path).parts

    if len(subs) == 2:  # noqa: PLR2004
        return subs[0], subs[1]

    return subs[0], str(Path(*subs[2:]))


@register.simple_tag
def node_module_asset(path: str):
    result = finder.find(path)

    if result is str:
        return static(path)

    package, target_file = resolve_path(path)
    deps = get_package_dependencies()

    final_path = None

    if deps and package in deps:
        file = next(node_modules_path.rglob(target_file))

        if file.exists():
            final_path = str(file.relative_to(node_modules_path))

    if not final_path:
        msg = f"'{path}' can't be found in '{node_modules_path}'."

        raise TemplateSyntaxError(msg)

    return static(final_path)
