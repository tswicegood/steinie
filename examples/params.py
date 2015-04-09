import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import app, routing

r = routing.Router()


class AddUpperCaseMessage(object):
    def __init__(self, app):
        pass

    def __call__(self, request, response, _next=None):
        request.params["upper_msg"] = request.params["msg"].upper()
        return _next(request, response)


r.use(AddUpperCaseMessage)


@r.param("msg")
def to_upper(param):
    return param.upper()


@r.get("/<msg:msg>")
def handler(request, response):
    return "Hello, {msg}".format(msg=request.params["msg"])

@r.get("/upper/<string:msg>")
def some_other_handler(request, response):
    return "Hello, {upper_msg} or {msg}".format(**request.params)


app = app.Steinie()
app.use("/", r)

if __name__ == "__main__":
    app.run()
