# Errors


class NodeJSNotFoundError(Exception):
    pass


class NPMNotFoundError(Exception):
    pass


class FailedToCreateFile(Exception):
    pass


class NonZeroExitCode(Exception):
    pass


class AlredyANPMPackageError(Exception):
    pass


class RuntimeNotFoundError(Exception):
    pass


class PlatformError(Exception):
    pass
