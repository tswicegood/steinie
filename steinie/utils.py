from functools import wraps


def generate_next(func, after):
    def next(*args, **kwargs):
        return after(*args, **kwargs)

    @wraps(func)
    def wrapped(*args, **kwargs):
        kwargs["_next"] = next
        return func(*args, **kwargs)
    return wrapped
