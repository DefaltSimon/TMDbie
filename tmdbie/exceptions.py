"""
Exceptions for TMDbie
"""

class TMDbException(Exception):
    """
    General exception, all other exceptions are subclassed
    """


class HTTPException(TMDbException):
    """
    Used when a Requestor encounters an error
    """
    pass


class DecodeError(TMDbException):
    """
    Used when invalid response is gotten
    """
    pass


class APIException(TMDbException):
    """
    General exception class when it's not a client problem
    """
    pass

class RatelimitException(APIException):
    """
    When you reach the ratelimit too many times (retries once by default)
    """
    pass