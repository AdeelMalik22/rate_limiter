class RateLimiter:

    def __init__(
        self,
        algorithm=None,
    ):
        if algorithm is not None:
            self.algorithm = algorithm

    def check(self, client_id):

        return self.algorithm.allow(
            client_id
        )