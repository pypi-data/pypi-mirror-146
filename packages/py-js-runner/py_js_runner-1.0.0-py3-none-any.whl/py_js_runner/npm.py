from subprocess import call as command
from .errors import NonZeroExitCode, NPMNotFoundError, AlredyANPMPackageError
from os import chdir, getcwd, mkdir, unlink, listdir
from shutil import rmtree


def run_command(command_to_run: str):
    status = command(command_to_run, shell=True)
    if status != 0:
        raise NonZeroExitCode(f"npm exited with error code: {status}")


class npm:
    def __init__(self):
        pass

    def install(self):
        run_command("npm install")

    def install_packages(self, *package_name: str, npm_args: str = ""):
        run_command("npm " + npm_args + " install " + "".join(package_name))

    def uninstall(self, *packages: str):
        run_command("npm uninstall " + "".join(packages))

    def check_npm(self):
        try:
            command("npm -v", shell=True)
        except:
            raise NPMNotFoundError(
                "npm not found. make sure npm is installed and added to path."
            )

    def init_npm_package(
        self,
        name: str,
        license: str = "MIT",
        author: str = "",
        description: str = "",
        version: str = "1.0.0",
        main: str = "index.js",
        npm_package_path: str = "./",
    ):
        package_json = """{
    "name": "<name>",
    "version": "<version>",
    "description": "<description>",
    "main": "<main>",
    "scripts": {
    "test": "echo \\\"Error: no test specified\\\" && exit 1"
},
    "keywords": [],
    "author": "<author>",
    "license": "<license>"
}
"""
        package_json = package_json.replace("<name>", name)
        package_json = package_json.replace("<version>", version)
        package_json = package_json.replace("<description>", description)
        package_json = package_json.replace("<main>", main)
        package_json = package_json.replace("<author>", author)
        package_json = package_json.replace("<license>", license)
        if self.check_if_npm_package(npm_package_path):
            raise AlredyANPMPackageError(f"{npm_package_path}: alredy a npm package.")

        else:
            old_pwd = getcwd()
            chdir(npm_package_path)
            package_json_file = open("package.json", "w")
            package_json_file.write(package_json)
            mkdir("./node_modules")
            chdir(old_pwd)

    def remove_npm_package(self, npm_package_path: str = "./"):
        old_pwd = getcwd()
        chdir(npm_package_path)
        rmtree("node_modules")
        unlink("./package.json")
        try:
            unlink("./package-lock.json")
        except:
            pass
        chdir(old_pwd)

    def check_if_npm_package(self, npm_package_path: str = "./"):
        dirs = listdir(npm_package_path)
        if "node_modules" in dirs and "package.json" in dirs:
            return True

        else:
            return False

    def npm_cli(self, args: str):
        run_command("npm " + args)
