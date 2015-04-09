import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import Steinie

app = Steinie()


@app.param("username")
def capitalize(param):
    return param.capitalize()


@app.get("/<username:some_user>")
def handler(request, response):
    return "Hello, %s\n" % request.params["some_user"]


if __name__ == "__main__":
    app.run()
