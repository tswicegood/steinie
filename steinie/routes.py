from functools import wraps
from werkzeug.routing import BaseConverter, Map, Rule

from . import exceptions


class Router(object):
    def __init__(self):
        self.map = Map()
        self.routes = {}

    def handle(self, request):
        urls = self.map.bind_to_environ(request.environ)
        endpoint, params = urls.match(request.path)

        def inner():
            request.params = params
            if request.method in self.routes[endpoint]._allowed_methods:
                return self.routes[endpoint](request)
            raise exceptions.Http405()
        return inner

    def get(self, route):
        def outer(fn):
            outer_id = str(fn)
            self.routes[outer_id] = fn
            rule = Rule(route, endpoint=outer_id)
            self.map.add(rule)

            fn._allowed_methods = ['GET', ]

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        return outer

    def param(self, name):
        def outer(fn):
            class BasicParameter(BaseConverter):
                def to_python(self, value):
                    return fn(value)

            self.map.converters[name] = BasicParameter

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        return outer
