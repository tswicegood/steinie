from functools import wraps
from werkzeug import routing
from werkzeug.routing import BaseConverter

from . import utils


def rule_dispatcher(rule, request, response):
    if getattr(rule, '_steinie_dispatchable', False):
        request.original_path = request.path
        request.path = request.original_path.replace(rule.bound_prefix, '')
        return rule.dispatch(request, response)
    try:
        return rule(request, response)
    except TypeError:
        return rule(request)


class Rule(routing.Rule):
    def __init__(self, *args, **kwargs):
        self._steinie_dispatchable = True
        self.func = kwargs.pop('func', None)
        self.router = kwargs.pop('router', None)
        super(Rule, self).__init__(*args, **kwargs)
        self.bound_prefix = None

    def dispatch(self, request, response):
        return utils.wrap_middleware_around_route(
            self.router.middleware,
            self.func,
            self.router
        )(request, response)

    def empty(self):
        rule = super(Rule, self).empty()
        rule.func = self.func
        rule.router = self.router
        return rule


class EndpointPrefix(routing.EndpointPrefix):
    pass


class Submount(routing.Submount):
    def get_rules(self, map):
        for rule in super(Submount, self).get_rules(map):
            rule.bound_prefix = self.path
            key = rule.rule
            if not key.startswith('/'):
                key = '/' + key
            map.router.routes[key] = rule
            yield rule


class Map(routing.Map):
    def __init__(self, router=None, *args, **kwargs):
        self.router = router
        super(Map, self).__init__(*args, **kwargs)


class Router(object):
    def __init__(self):
        self.map = Map(self)
        self.converters = {}
        self.routes = {}
        self.middleware = []

    def handle(self, request, response):
        urls = self.map.bind_to_environ(request.environ)
        endpoint, params = urls.match(request.path)

        # All endpoints should start with a slash
        if not endpoint[0].startswith('/'):
            endpoint = '/' + endpoint

        request.params = params
        rule = self.routes[endpoint]
        print("dispatching %s" % rule)
        return rule_dispatcher(rule, request, response)

    def method(self, route, methods=None):
        def outer(fn):
            self.routes[route] = fn
            rule = Rule(route, endpoint=route, methods=methods, func=fn,
                        router=self)
            self.map.add(rule)

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner

        return outer

    def post(self, route):
        return self.method(route, methods=['POST', ])

    def get(self, route):
        return self.method(route, methods=['GET', ])

    def head(self, route):
        return self.method(route, methods=['HEAD', ])

    def info(self, route):
        return self.method(route, methods=['INFO', ])

    def options(self, route):
        return self.method(route, methods=['OPTIONS', ])

    def patch(self, route):
        return self.method(route, methods=['PATCH'])

    def put(self, route):
        return self.method(route, methods=['PUT'])

    def param(self, name):
        def outer(fn):
            class BasicParameter(BaseConverter):
                def to_python(self, value):
                    return fn(value)

            self.map.converters[name] = BasicParameter
            self.converters[name] = fn

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        return outer

    def use(self, *args):
        if len(args) == 1:
            self.middleware.append(args[0])

        if len(args) == 2:
            route, router = args
            self.add_router(route, router)

    def add_router(self, route, router):
        if route.startswith('/'):
            route = route[1:]
        submount = route
        if not submount.startswith('/'):
            submount = '/' + submount
        rules = [a for a in router.map.iter_rules()]

        mount = EndpointPrefix(route, [Submount(submount, rules)])
        for name, fn in router.converters.items():
            self.param(name)(fn)
        self.map.add(mount)
