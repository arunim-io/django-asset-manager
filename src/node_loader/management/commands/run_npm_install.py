# ruff: noqa: S404, S603

from subprocess import CalledProcessError, check_output

from node_loader.conf import settings

from django.core.management.base import BaseCommand


class NodePackageContext:
    def __init__(self):
        self.package_json = settings.node_modules_path.parent.joinpath("package.json")

    def __enter__(self):
        if not self.package_json.exists():
            self.package_json.symlink_to(settings.package_json_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.package_json.is_symlink():
            self.package_json.unlink()
        return False


class Command(BaseCommand):
    help = "Alias for npm install"

    def handle(self, *args, **options):
        if not settings.package_json_path.exists():
            self.stderr.write(
                f"`{settings.package_json_path}` couldn't be found. Exiting..."
            )
        if not settings.node_modules_path.exists():
            self.stderr.write(
                f"{settings.node_modules_path} doesn't exist. Creating now..."
            )
            settings.node_modules_path.mkdir(parents=True)

        npm_exe = settings.package_manager.exe_path

        if not npm_exe:
            self.stderr.write(
                f"{settings.package_manager.name} not found. Is it installed in your system?"  # noqa: E501
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
                        cwd=settings.node_modules_path.parent,
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
