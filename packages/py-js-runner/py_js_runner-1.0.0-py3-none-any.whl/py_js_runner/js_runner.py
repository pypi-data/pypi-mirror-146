# JS Runner

# Imports
from subprocess import call as command
from os import unlink

# Errors
from .errors import (
    AlredyANPMPackageError,
    NodeJSNotFoundError,
    FailedToCreateFile,
    NonZeroExitCode,
)


class javascript:
    def __init__(self):
        pass

    def check_node(self):
        try:
            command("node -v", shell=True)

        except:
            raise NodeJSNotFoundError(
                "node.js not found. make sure node.js is installed and added to path."
            )

    def run(self, code: str):
        try:
            temp_file = open("pyjstempfile.js", "w")
            temp_file.write(code)
            temp_file.close()
        except:
            raise FailedToCreateFile("failed to create temporary javascript file.")

        node_exit_status = command("node pyjstempfile.js", shell=True)
        if node_exit_status != 0:
            raise NonZeroExitCode(f"node.js exited with error code: {node_exit_status}")

        unlink("./pyjstempfile.js")
