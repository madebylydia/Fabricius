from fabricius.exceptions.base import FabriciusException


class InvalidTemplateException(FabriciusException):
    """
    Base class for all exceptions related to templates that are not valid.
    """
