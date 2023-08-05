"""This module include some custom exceptions."""


class RezBuildException(Exception):
    """The parent exception of all the custom exceptions."""

    pass


class ArgumentError(RezBuildException):
    """When the argument invalid."""

    pass


class FileAlreadyExistError(RezBuildException):
    """When the file already exist."""

    pass


class FileNotExistError(RezBuildException):
    """When the file does not exist."""

    pass


class ReNotMatchError(RezBuildException):
    """When the regex does not match."""

    pass


class UnsupportedError(RezBuildException):
    """When something unsupported."""

    pass
