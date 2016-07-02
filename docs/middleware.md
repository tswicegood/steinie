# Middleware

Middleware provides a place for you to modify every request for a given router
instance.  All middleware is [router][] specific, so its effects are only present
for the router it is mounted to.

## Using Middleware

You use `router.use` to add middleware to a router instance just like you do
when [mounting another router][router-mount].  The key difference is that you
*do not* provide a URL pattern to match again.  Instead, you simply provide
the middleware class.  For example, if you had a `UserMiddleware` class, you
would do:

```python
router.use(UserMiddleware)
```

Steinie middleware is different than WSGI middleware, but you can use regular
WSGI middleware with Steinie by wrapping the `Steinie` instance.  Steinie's
middleware provides the advantage of not having to create `Request` and
`Response` objects to interact with it, but it does not provide interoperability
with other WSGI frameworks.


## Custom Middleware

Writing your own middleware is simple.  It requires an object that accepts a
single parameter at instantiation and is callable taking three arguments:
`request`, `response`, and `_next`.

Here's a simple middleware that looks for the parameter `msg` and converts it
to upper case.

```python
class UppercaseMiddleware(object):
    def __init__(self, router):
        pass  # We don't need the router for this

    def __call__(self, request, response, _next):
        if "msg" in request.params:
            request.params["msg_upper"] = request.params["msg"].upper()
        return _next(request, response)
```

The `_next` argument provided to `__call__` is your way of controlling the way
this request is responded to.  Whatever you return from `__call__` is what


## Middleware vs. Parameters
Both middleware and parameters can be used to achieve very similar goals, but
they have separate roles to play when processing a request.

### Middleware
These are global and have the chance to modify every incoming request.  They
have the full request and have the ability to circumvent the normal response.
Use them when you need to modify *every* request that is processed for a given
route or you need to do more than change part of the request URL to some other
object.

### Parameters
These are localized to routes that have the parameter in the request URL.
Unlike middleware, all they can do is transform part of a URL into something
else.  They're very useful when translating an ID to an object in the database
or some other similar transformation, but they won't let you change the
response that Steinie returns.

[router]: routers.md
[router-mount]: routers.md#mounting-routers
