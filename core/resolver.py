class KeyResolver:

    def __init__(self, func=None):
        self.func = func


    def resolve(self, *args, **kwargs):

        if self.func:
            return self.func(*args, **kwargs)


        # auto detect request object
        for arg in args:

            if hasattr(arg, "client"):
                return arg.client.host


        for value in kwargs.values():

            if hasattr(value, "client"):
                return value.client.host



        return "anonymous"