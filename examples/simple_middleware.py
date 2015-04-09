import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from steinie import app


class Middleware(object):
    def __init__(self, app):
        pass

    def __call__(self, request, response, _next):
        response.data = "MIDDLEWARE INVOKED"
        return response

a = app.Steinie()
a.use(Middleware)

if __name__ == "__main__":
    a.run()
