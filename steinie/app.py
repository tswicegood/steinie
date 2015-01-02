from werkzeug import serving
from werkzeug import wrappers

from . import routes


class Steinie(routes.Router):
    def __init__(self, host="127.0.0.1", port=5151):
        self.host = host
        self.port = port
        super(Steinie, self).__init__()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = wrappers.Request(environ)
        fn = self.handle(request)
        return wrappers.Response(fn())(environ, start_response)

    def run(self):
        serving.run_simple(self.host, self.port, self, use_debugger=True)
