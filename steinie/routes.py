from werkzeug.routing import BaseConverter, Map, Rule
from . import responses


class Router(object):
    def __init__(self):
        self.map = Map()
        self.routes = {}

    def find_for(self, request):
        urls = self.map.bind("example.com", "/")
        endpoint, params = urls.match(request.url)

        def inner():
            request.params = params
            return self.routes[endpoint](request)
        return inner

    def get(self, route):
        def outer(f):
            outer_id = str(f)
            self.routes[outer_id] = f
            rule = Rule(route, endpoint=outer_id)
            self.map.add(rule)

            def inner(*args, **kwargs):
                return f(*args, **kwargs)
            return inner
        return outer

    def param(self, name):
        def outer(fn):
            class BasicParameter(BaseConverter):
                def to_python(self, value):
                    return fn(value)

            self.map.converters[name] = BasicParameter
        return outer


class Route(object):
    def __init__(self, path, methods):
        self.path = path
        self.methods = methods

    def __lt__(self, request):
        if not self.path_matches(request):
            return False
        if not self.is_allowed_method(request):
            raise responses.Http405

        request.route = self
        self.request = request
        return True

    def path_matches(self, request):
        return self.path == request.path

    def is_allowed_method(self, request):
        return request.method in self.methods


def route(path, methods="GET"):
    if not type(methods) is list:
        methods = [methods, ]
    return Route(path, methods)


def get(path):
    return route(path, methods=["GET"])

