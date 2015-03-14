from werkzeug import serving
from werkzeug import wrappers

from . import routing


class Steinie(routing.Router):
    def __init__(self, host="127.0.0.1", port=5151, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        super(Steinie, self).__init__()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        for middleware_class in self.middleware:
            response = middleware_class(self)(environ, start_response)
            if response:
                return wrappers.Response(response)(environ, start_response)
        request = wrappers.Request(environ)
        request._steinie = {
            "environ": environ,
            "start_response": start_response,
        }
        response = self.handle(request)
        return wrappers.Response(response)(environ, start_response)

    def run(self):
        serving.run_simple(self.host, self.port, self, use_debugger=self.debug)
