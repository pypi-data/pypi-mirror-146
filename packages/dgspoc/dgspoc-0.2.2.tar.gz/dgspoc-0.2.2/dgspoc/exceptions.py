"""Module containing the exception class for describe-get-system proof of concept module."""


class DGSError(Exception):
    """Use to capture error DGS construction."""


class TemplateStorageError(DGSError):
    """Use to capture error for TemplateStorage."""


class AdaptorAuthenticationError(DGSError):
    """Use to capture error for adaptor connection"""


class InterpreterError(DGSError):
    """Use to capture error for interpreter"""


class NotImplementedFrameworkError(InterpreterError):
    """Use to capture error for not implement framework"""


class ComparisonOperatorError(InterpreterError):
    """Use to capture error for invalid comparison operator"""


class ConnectDataStatementError(InterpreterError):
    """Use to capture error for interpreting connect data statement"""


class UseTestcaseStatementError(InterpreterError):
    """Use to capture error for interpreting use testcase statement"""


class ConnectDeviceStatementError(InterpreterError):
    """Use to capture error for interpreting connect device statement"""


class DisconnectDeviceStatementError(InterpreterError):
    """Use to capture error for interpreting disconnect device statement"""


class ReleaseDeviceStatementError(InterpreterError):
    """Use to capture error for interpreting release device statement"""


class ReleaseResourceStatementError(InterpreterError):
    """Use to capture error for interpreting release resource statement"""
