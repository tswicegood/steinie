# Routers

Routers are the key construct of Steinie.  Everything is a router or interacting
with a router.

The `Router` object is imported directly from `steinie` and has to be
instantiated before use like this:

```python
from steinie import Router
router = Router()
```

It provides decorators for all of the standard HTTP methods.  Each method is
available as a decorator by the same name as the method in lower case:

* GET
* POST
* DELETE
* HEAD
* INFO
* OPTIONS
* PATCH
* PUT
* TRACE


## Example Routes

Here are a few example routes.  You can response to a GET request to
`/username/` like this:

```python
@router.get("/<username>/")
def handle_user(request, response):
    return "Your user is %s" % request.params["username"]
```

Note that a `POST` request won't work.  To do that, you need to add a route
with that decorator like this:

```python
@router.post("/<username>/")
def handle_user_post(request, response):
    return "You sent a POST here %s" % request.params["username"]
```

Both of these routes show the parameter syntax.  It builds on top of Werkzeug's
notion of a converters in [url routing][werk-routing].  All of Werkzeug's
[built-in converters][werk-converter] are available for use inside Steinie and
you can write your own.


## Custom Parameters
You can add custom parameters to any router using the `param` decorator.  These
are then run on any incoming requests that have the pattern inside their URL
route.  For example, to convert a username string to a user as found inside a
dictionary in memory:

```python
@router.param("username")
def load_user(param):
    try:
        return user_cache[param]
    except IndexError:
        return None
```

Now you can access this via:

```python
@router.get("/<username:user>/")
def handle_request(request, response):
    return "Your name: %s" % request.params["user"].get_full_name()
```


## Mounting Routers
*TODO*

## Looking up Routes
*TODO*

[werk-converter]: http://werkzeug.pocoo.org/docs/0.10/routing/#builtin-converters
[werk-routing]: http://werkzeug.pocoo.org/docs/0.10/routing/
