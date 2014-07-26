from . import views


def route(f):
    class Callable(object):
        def __call__(self, *args, **kwargs):
            return views.View(f)
    return Callable()
