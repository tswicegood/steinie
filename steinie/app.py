from werkzeug import serving
from werkzeug import wrappers

from . import routes


class Steinie(routes.Router):
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = wrappers.Request(environ)
        fn = self.find_for(request)
        return wrappers.Response(fn())(environ, start_response)

    def run(self):
        host = "localhost"
        port = 5151
        serving.run_simple(host, port, self, use_debugger=True)
