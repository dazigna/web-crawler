class WebCrawlerException(Exception):
    """Base exception class for web crawler errors."""

    def __init__(self, message):
        super().__init__(message)


class RateLimitException(WebCrawlerException):
    """Raised when crawler hits rate limits."""

    pass


class RedirectException(WebCrawlerException):
    """Raised when crawler hits rate limits."""

    def __init__(self, message, redirect_url=None, status_code=None):
        self.redirect_url = redirect_url
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(WebCrawlerException):
    """Raised when crawler hits rate limits."""

    pass


class InvalidBaseURL(WebCrawlerException):
    """Raised when the base URL is invalid."""

    pass


class GenericCrawlerException(WebCrawlerException):
    """Raised when an unknown error occurs."""

    pass
