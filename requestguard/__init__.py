"""
RateGuard — Lightweight rate limiting for FastAPI.

Quick start:

    from requestguard import limit

    @limit(requests=5, window=60)
    def my_endpoint(request: Request):
        return {"status": "ok"}
"""

from requestguard.decorators.decorator import limit
from requestguard.core.policy import RateLimitPolicy
from requestguard.core.limiter import RateLimiter
from requestguard.core.resolver import KeyResolver
from requestguard.storage.storage import MemoryStorage
from requestguard.algorithms.fixed_window import FixedWindowLimiter
from requestguard.core.exceptions import RateLimitExceeded

__all__ = [
    "limit",
    "RateLimitPolicy",
    "RateLimiter",
    "KeyResolver",
    "MemoryStorage",
    "FixedWindowLimiter",
    "RateLimitExceeded"
]

__version__ = "0.1.0"
__author__ = "AdeelMalik22"
