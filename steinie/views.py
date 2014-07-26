from werkzeug import wrappers

from . import responses


class View(responses.HttpResponse):
    def __init__(self, func):
        self.func = func

    def __lt__(self, route):
        self.route = route
        self.request = self.route.request
        raise self

    def do(self, environ, start_response):
        response = self.func(self.request)
        return wrappers.Response(response, mimetype="text/html")(
            environ, start_response)
