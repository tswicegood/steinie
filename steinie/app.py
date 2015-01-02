from werkzeug import serving
from werkzeug import wrappers

from . import responses
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


def create_app(callback):
    def app(environ, start_response):
        request = wrappers.Request(environ)
        try:
            callback(request)

            # `callback` should have bailed by now with a response, so
            # we haven't found anything
            response = responses.Http404()
            return response.do(environ, start_response)

        except responses.HttpResponse as response:
            return response.do(environ, start_response)
    return app
