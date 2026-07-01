
class RateLimitExceeded(Exception):
    """Raised when a rate limit is exceeded. Framework-agnostic."""
    def __init__(self, retry_after=None, message="Too many requests"):
        self.message = message
        self.retry_after = retry_after
        self.detail = {"error": message, "retry_after": retry_after}
        super().__init__(message)