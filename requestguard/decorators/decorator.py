from functools import wraps
from requestguard.core.exceptions import RateLimitExceeded
from requestguard.core.policy import RateLimitPolicy
from requestguard.storage.storage import MemoryStorage
from requestguard.algorithms.fixed_window import FixedWindowLimiter
from requestguard.core.limiter import RateLimiter
from requestguard.core.resolver import KeyResolver

storage = MemoryStorage()

def limit(max_retries, ttl, key=None):
    policy = RateLimitPolicy(limit=max_retries, window_seconds=ttl)
    algorithm = FixedWindowLimiter(policy, storage)
    limiter = RateLimiter(algorithm)
    resolver = KeyResolver(key)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_id = resolver.resolve(*args, **kwargs)
            rl_key = f"{func.__name__}:{client_id}"

            result = limiter.check(rl_key)
            if not result["allowed"]:
                raise RateLimitExceeded(retry_after=result.get("retry_after"))

            return func(
                *args,
                **kwargs
            )


        return wrapper
    return decorator