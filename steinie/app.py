from werkzeug import serving
from werkzeug import wrappers

from . import routing
from . import utils


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
        new_response = utils.wrap_middleware_around_route(
            self.middleware,
            self.handle,
            self
        )(request, response)
        if not isinstance(new_response, wrappers.Response):
            if type(new_response) is tuple:
                response.status_code, response.data = new_response
            else:
                if new_response is None:
                    new_response = ""
                response.data = new_response
        else:
            response = new_response
        return response(environ, start_response)

    def run(self):
        serving.run_simple(self.host, self.port, self, use_debugger=self.debug)
