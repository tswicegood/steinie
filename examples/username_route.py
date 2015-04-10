import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import Steinie, Router

app = Steinie()
route = Router()


@route.param("username")
def capitalize(param):
    return param.capitalize()


@route.get("/<username:some_user>")
def handler(request, response):
    return "Hello, %s\n" % request.params["some_user"]


app.use("/user", route)

if __name__ == "__main__":
    app.run()
