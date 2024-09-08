# ruff: noqa: S404, S603

from subprocess import CalledProcessError, check_output

from django_node_loader.conf import settings

from django.core.management.base import BaseCommand


class NodePackageContext:
    def __init__(self):
        self.package_json = settings.NODE_MODULES_PATH.parent.joinpath("package.json")

    def __enter__(self):
        if not self.package_json.exists():
            self.package_json.symlink_to(settings.PACKAGE_JSON_PATH)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.package_json.is_symlink():
            self.package_json.unlink()
        return False


class Command(BaseCommand):
    help = "Alias for npm install"

    def handle(self, *args, **options):
        if not settings.PACKAGE_JSON_PATH.exists():
            self.stderr.write(
                f"`{settings.PACKAGE_JSON_PATH}` couldn't be found. Exiting..."
            )
        if not settings.NODE_MODULES_PATH.exists():
            self.stderr.write(
                f"{settings.NODE_MODULES_PATH} doesn't exist. Creating now..."
            )
            settings.NODE_MODULES_PATH.mkdir(parents=True)

        npm_exe = settings.PACKAGE_MANAGER.EXE_PATH

        if not npm_exe:
            self.stderr.write(
                f"{settings.PACKAGE_MANAGER.NAME} not found. Is it installed in your system?"  # noqa: E501
            )
        else:
            with NodePackageContext():
                self.stdout.write("Installing dependencies", self.style.NOTICE)

                try:
                    output = check_output(
                        [
                            npm_exe,
                            "install",
                            "--no-package-lock",
                            "--omit dev",
                        ],
                        cwd=settings.NODE_MODULES_PATH.parent,
                        encoding="utf-8",
                    )
                except CalledProcessError as err:
                    self.stderr.write(f"Error occured while running npm, {err}")
                finally:
                    self.stdout.write(output)
                    self.stdout.write(
                        "All dependencies have been successfully installed.",
                        self.style.SUCCESS,
                    )
