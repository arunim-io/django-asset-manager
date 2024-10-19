from pathlib import Path

from django.template import Library, TemplateSyntaxError
from django.templatetags.static import static

from asset_manager.conf import settings
from asset_manager.staticfiles.finders import NodeModulesFinder

register = Library()
finder = NodeModulesFinder()
node_modules_path = settings.node_modules_path


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
    deps = settings.package_dependencies

    final_path = None

    if deps and package in deps:
        file = next(node_modules_path.rglob(target_file))

        if file.exists():
            final_path = str(file.relative_to(node_modules_path))

    if not final_path:
        msg = f"'{path}' can't be found in '{node_modules_path}'."

        raise TemplateSyntaxError(msg)

    return static(final_path)
