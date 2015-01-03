from werkzeug import routing
from werkzeug import serving
from werkzeug import wrappers

from . import routes


class Steinie(routes.Router):
    def __init__(self, host="127.0.0.1", port=5151, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        super(Steinie, self).__init__()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = wrappers.Request(environ)
        response = self.handle(request)
        return wrappers.Response(response)(environ, start_response)

    def run(self):
        serving.run_simple(self.host, self.port, self, use_debugger=self.debug)

    def use(self, route, router):
        if route.startswith('/'):
            route = route[1:]
        submount = route
        if not submount.startswith('/'):
            submount = '/' + submount
        rules = [a for a in router.map.iter_rules()]

        mount = routing.EndpointPrefix(route, [routes.Submount(submount, rules)])
        self.map.add(mount)
