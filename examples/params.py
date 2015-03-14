import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import app, routing

r = routing.Router()


@r.param("msg")
def to_upper(param):
    return param.upper()


@r.get("/<msg:msg>")
def handler(request, response):
    return "Hello, {msg}".format(msg=request.params["msg"])


app = app.Steinie()
app.use("/", r)

if __name__ == "__main__":
    app.run()
