from functools import wraps


def req_or_res(func):
    def inner(request, response, **kwargs):
        try:
            return func(request, response, **kwargs)
        except TypeError as e:
            return func(request, **kwargs)
    return inner


def wrap_all_funcs(*funcs):
    next_func = None
    for func in reversed(funcs):
        if next_func is None:
            next_func = func
            continue
        next_func = generate_next(func, next_func)
    return next_func


def generate_next(func, after):
    def next(*args, **kwargs):
        return after(*args, **kwargs)

    @wraps(func)
    def wrapped(*args, **kwargs):
        kwargs["_next"] = next
        return func(*args, **kwargs)
    return wrapped
