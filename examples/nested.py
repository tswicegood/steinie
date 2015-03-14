import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import app, routing

r = routing.Router()


@r.get("/foo")
def handle_foo(request, response):
    return "\n".join([
        "request.path: %s" % request.path,
        "request.original_path: %s" % request.original_path,
    ])

app = app.Steinie()
app.use("/bar", r)

if __name__ == "__main__":
    app.run()
