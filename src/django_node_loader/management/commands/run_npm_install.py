from shutil import which
from subprocess import CalledProcessError, check_output

from django.core.management.base import BaseCommand

from ...conf import settings


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
            self.stdout.write(
                f"{settings.NODE_MODULES_PATH} doesn't exist. Creating now..."
            )
            settings.NODE_MODULES_PATH.mkdir(parents=True)

        npm_exe = which("npm")

        if not npm_exe:
            self.stderr.write("npm not found. Is it installed in your system?")
        else:
            with NodePackageContext():
                self.stdout.write(self.style.NOTICE("Installing dependencies"))

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

                self.stdout.write(output)
                self.stdout.write(
                    self.style.SUCCESS(
                        "All dependencies have been successfully installed."
                    )
                )
