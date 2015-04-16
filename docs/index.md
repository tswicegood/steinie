# Steinie

Steinie is your little framework for building HTTP applications

## Quick Start

```console
pip install steinie
```

Create a file called `server.py` and add this to it:

```python
from steinie import Steinie
app = Steinie()


@app.param("msg")
def msg(param):
    return param.capitalize()


@app.get("/<msg:some_message>")
def handler(request, response):
    return "You said %s", request.params["some_message"]


if __name__ == "__main__":
    app.run()
```

Run this file, and you're off to the races.


## Why use this?
Because you need a simple, straight forward, well-tested HTTP framework to
build your micro-services with.

### Key Features

#### Everything is a Router

It uses the same everything-is-a-router pattern found in [Express v4 and
up][Express].  For those who aren't familiar with the pattern, everything you
build is a router.  Routers are isolated from the rest of your application and
can be mounted *anywhere* by other routers or the application.

This nested control lets you build segments of your HTTP application that don't
effect the rest of your application.  Finally, you can mount middleware to do
something like authentication control for the parts of your application that
require it, not the entire site!  [More on routes.](#TODO)


#### Simple, Pythonic constructs

Every you need is passed in to you at each step of the way.  There's no need to
import variables to get your request.  It's provided as the first argument for
every middleware or route handler.  [More on route handlers.](#TODO)


#### Wrapped Middleware

The WSGI `environ` and `start_response` functions allow you to write
WSGI-middleware, but that means you have to understand how WSGI works in
addition to whatever other layer of code your framework of choice puts in
place.

Steinie's built-in middleware takes the same parameters as your route handler
with one exception, an added third function that you use to continue executing
the request as its configured.  [More on middleware.](#TODO)


#### Powered by Werkzeug

Steinie builds on top of [Werkzeug][].  Whenever you need more than Steinie
gives you, simply drop back to Werkzeug as needed (but [open a feature request
first][feature-req]).


[Express]: http://expressjs.com/
[Werkzeug]: http://werkzeug.pocoo.org/
[feature-req]: https://github.com/tswicegood/steinie/issues/new?labels[]=enhancement
