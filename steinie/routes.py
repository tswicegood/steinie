from functools import wraps
from werkzeug import routing
from werkzeug.routing import BaseConverter


def rule_dispatcher(rule, request):
    if hasattr(rule, 'func'):
        request.original_path = request.path
        request.path = request.original_path.replace(rule.bound_prefix, '')
        return rule.func(request)
    return rule(request)


class Rule(routing.Rule):
    def __init__(self, string=None, func=None, *args, **kwargs):
        super(Rule, self).__init__(string, *args, **kwargs)
        self.func = func
        self.bound_prefix = None

    def empty(self):
        rule = super(Rule, self).empty()
        rule.func = self.func
        return rule


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
        self.routes = {}

    def handle(self, request):
        urls = self.map.bind_to_environ(request.environ)
        endpoint, params = urls.match(request.path)

        # All endpoints should start with a slash
        if not endpoint[0].startswith('/'):
            endpoint = '/' + endpoint

        request.params = params
        rule = self.routes[endpoint]
        return rule_dispatcher(rule, request)

    def method(self, route, methods=None):
        def outer(fn):
            self.routes[route] = fn
            rule = Rule(route, endpoint=route, methods=methods, func=fn)
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
