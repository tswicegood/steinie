import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import Steinie, Router

app = Steinie()
route = Router()


class CapitalizeMiddleware(object):
    def __init__(self, route):
        pass

    def __call__(self, request, response, _next):
        if "some_user" in request.params:
            new = request.params["some_user"].capitalize()
            request.params["some_user"] = new
        return _next(request, response)

route.use(CapitalizeMiddleware)


@route.get("/<some_user>")
def handler(request, response):
    return "Hello, %s\n" % request.params["some_user"]


app.use("/user", route)

if __name__ == "__main__":
    app.run()
