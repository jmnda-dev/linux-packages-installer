import subprocess
from app import console


class PackageInstaller:
    def __init__(self, pkg_name=None, pkg_slug=None, command=None):
        self.pkg_name = pkg_name
        self.pkg_slug = pkg_slug
        self.command = command

    def install_package(self):
        with console.status(
            f"[bold cyan reverse]Installing package {self.pkg_name} - {self.pkg_slug}[/]",
            spinner="point",
        ):
            subprocess.run(self.command, shell=True)
