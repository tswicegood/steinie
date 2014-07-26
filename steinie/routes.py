from . import responses


class Route(object):
    def __init__(self, path, methods):
        self.path = path
        self.methods = methods

    def __lt__(self, request):
        if not self.path_matches(request):
            return False
        if not self.is_allowed_method(request):
            raise responses.Http405

        request.route = self
        self.request = request
        return True

    def path_matches(self, request):
        return self.path == request.path

    def is_allowed_method(self, request):
        return request.method in self.methods


def route(path, methods="GET"):
    if not type(methods) is list:
        methods = [methods, ]
    return Route(path, methods)


def get(path):
    return route(path, methods=["GET"])

