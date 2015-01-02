from werkzeug import wrappers

from . import responses
from . import routes


class Steinie(routes.Router):
    pass


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
