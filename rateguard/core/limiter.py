from rateguard.core.policy import RateLimitPolicy
from rateguard.storage.storage import MemoryStorage
from rateguard.algorithms.fixed_window import FixedWindowLimiter


class RateLimiter:

    def __init__(
        self,
        algorithm=None,
        max_retries: int = None,
        ttl: int = None
    ):
        if algorithm is not None:
            self.algorithm = algorithm
        elif max_retries is not None and ttl is not None:
            policy = RateLimitPolicy(limit=max_retries, window_seconds=ttl)
            self.algorithm = FixedWindowLimiter(policy, MemoryStorage())
        else:
            raise ValueError("Must provide either algorithm or both max_retries and ttl")


    def check(self, client_id):

        return self.algorithm.allow(
            client_id
        )