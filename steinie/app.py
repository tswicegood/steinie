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
        request = wrappers.Request(environ)
        response = wrappers.Response()
        for middleware_class in self.middleware:
            new_response = middleware_class(self)(request, response)
            if new_response:
                return new_response(environ, start_response)
        new_response = self.handle(request, response)
        if not isinstance(new_response, wrappers.Response):
            response.data = new_response
        else:
            response = new_response
        return response(environ, start_response)

    def run(self):
        serving.run_simple(self.host, self.port, self, use_debugger=self.debug)
