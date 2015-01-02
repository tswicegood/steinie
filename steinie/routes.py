from functools import wraps
from werkzeug.routing import BaseConverter, Map, Rule


class Router(object):
    def __init__(self):
        self.map = Map()
        self.routes = {}

    def find_for(self, request):
        if getattr(request, 'environ', False):
            # print("binding to environ")
            urls = self.map.bind_to_environ(request.environ)

        # TODO This is test-specific code, need to rework
        else:
            urls = self.map.bind("example.com", "/")
        endpoint, params = urls.match(request.path)

        def inner():
            request.params = params
            return self.routes[endpoint](request)
        return inner

    def get(self, route):
        def outer(fn):
            outer_id = str(fn)
            self.routes[outer_id] = fn
            rule = Rule(route, endpoint=outer_id)
            self.map.add(rule)

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
