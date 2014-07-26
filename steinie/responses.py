from werkzeug import wrappers


class HttpResponse(BaseException):
    pass


class Http405(HttpResponse):
    def do(self, environ, start_response):
        return wrappers.Response(status=405)(environ, start_response)


class Http404(HttpResponse):
    def do(self, environ, start_response):
        return wrappers.Response(status=404)(environ, start_response)
