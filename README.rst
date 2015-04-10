steinie
=======
A little framework for doing web applications


Usage
-----
Steinie is built around the concept of routes.  Your application is made up of
one or more routes that guide the web request through your code.  Let's start
with the simplest of simple, the Hello World web application.

.. code-block:: python

    from steinie import Steinie
    app = Steinie()


    @app.get("/")
    def get(request, response):
        return "Hello World, from Steinie!\n"


    if __name__ == "__main__":
        app.run()


You can run this directly using ``python`` if you save this to a file.  This
starts up a simple development server on port 5151 that responds to the ``/``
route on your local computer.  Give it a try.

Steinie uses `Werkzeug`_ for handling its routes.  This means all of your
familiar route patterns are available to you inside Steinie.

Steinie has built-in decorators for ``GET`` and ``POST`` along with ``DELETE``,
``HEAD``, ``INFO``, ``OPTIONS``, ``PATCH``, ``PUT``, and ``TRACE``.


Dealing with Parameters
"""""""""""""""""""""""
Another common need is to provide parameters to your web application.  Lets say
you wanted to add a ``username`` to your path, but you wanted it capitalized
(bear with me for a minute), you can do that with the ``param`` decorator like
this:

.. code-block:: python

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

Using the ``param`` decorator, you specify the name of the parameter you want
to create, then you provide a function specifying what you want to do.  You can
run this example, then load ``http://localhost:5151/alice`` and it will respond
with "Hello, Alice!"

If you're familiar with Flask's (and by extension, Werkzeug's) converters this
might look very familiar.  Again, building off of the Werkzeug base, much of
what's provided here mimics what you might already be used to.

Now that you've seen the basic example, imagine instead if your created a
function that loads a user object from your database and returns that.  Using
the ``params`` decorator, you can start to turn basic parameters from your
incoming request into something that matches the way you've modeled your actual
application.


Grouping routes and parameters
""""""""""""""""""""""""""""""
You might be wondering how this scales.  A single file with a ton of decorated
functions sound pretty unwieldy to me.  Thankfully, Steinie provides a way to
break up your functionality into logical parts through what it calls a
``Router``.

Let's enhance the example above.  Most of what's there relates to users, so
we're going to create a new ``Route``, then mount it to ``/user``.

First, adjust the import statement so it looks like this:

.. code-block:: python

    from steinie import Steinie, Router

Next, create a new ``route`` object from the ``Router`` and adjust your two
decorated functions to use that.  It should look like this:

.. code-block:: python

    route = Router()


    @route.param("username")
    def capitalize(param):
        return param.capitalize()


    @route.get("/<username:some_user>")
    def handler(request, response):
        return "Hello, %s\n" % request.params["some_user"]


Finally, you need to modify your ``app`` object to use this your new route.
You do that with the aptly named ``use`` method like this:

.. code-block:: python

    app.use("/user", route)

Save your work, fire up your code, then visit your server again.  If you try
to go to ``http://localhost:5151/alice`` again you'll get a 404.  Instead, you
need to add ``/user`` to the URL so it looks like this:
``http://localhost:5151/user/alice``.


Dealing with Middleware
"""""""""""""""""""""""
There's one more part to becoming an expert in Steine: Middleware.  Middleware
gives you a chance to modify the request or response for every incoming request.

Let's continue to build on our example above.  Instead of using the ``param``
decorator, let's create a middleware that capitalizes all ``some_user``
parameters.

First, let's create the middleware.  Steinie expects them to be objects that can
be intantiated and provided a ``Router`` instance, then invoked via the
``__call__`` method.  That's it.  Add this to your file and then you can say
you've created your very own Steinie middleware:

.. code-block:: python

    class CapitalizeMiddleware(object):
        def __init__(self, route):
            pass

        def __call__(self, request, response, _next):
            if "some_user" in request.params:
                new = request.params["some_user"].capitalize()
                request.params["some_user"] = new
            return _next(request, response)

There's a couple of things to call out here.  First, we don't need the ``route``
provided at instantiation time, so there's no need to store it. If you did, you
could set that as an attribute on the class.

Next up, the ``__call__`` method has three arguments.  ``request`` and
``response`` are familiar from earlier, but ``_next`` is new.  This is a
function generated by Steinie that allows the middleware to control what happens
when it's invoked.  For our purposes here, we want to modify the ``some_user``
value by capitalizing it when it's present, then continue on.  To do that, you
simply return the result of ``_next(request, response)``.

The ability to control what happens here is a key part of Steinie's middleware.
You can capture the return value from ``_next`` and do something with it.  Use
cases that jump to mind for me are a ``CacheMiddleware`` that attempts to load
a request from cache and returns that if its found but will allow the request
to go through if it hasn't been cached.

This simple example here is just that, pretty simple.

You're not quite finished with the middleware yet.  Next you need to tell your
router to use it.  Enter ``router.use`` again:

.. code-block:: python

    route.use(CapitalizeMiddleware)

This is the same method you used to attach a router to an application, but
this time there's no route (the first argument you used above) associated with
it.  Providing ``router.use`` with a single argument signals to Steinie that
you're giving it a middleware that it should execute when dealing with all
requests this router attempts to handle.

The final modification that you should make is to remove the params function
and adjust your ``get`` route.  When it's finished, it should look like this:

.. code-block:: python

    @route.get("/<some_user>")
    def handler(request, response):
        return "Hello, %s\n" % request.params["some_user"]

Now, re-run your code and access it.  You should get the same output, but this
is a different pattern.  What makes one pattern over the other better?  Funny
you should mention it, that's the next topic.


Middleware vs. Parameters
"""""""""""""""""""""""""
Both middleware and parameters can be used to acheive very similar goals, but
they have distinct roles.

Middleware
  These are global and have the chance to modify every incoming request.  They
  have the full request and have the ability to circumvent the normal response.
  Use them when you need to modify *every* request that is processed for a given
  route or you need to do more than change part of the request URL to some other
  object.

Parameters
  These are localized to routes that have the parameter in the request URL.
  Unlike middleware, all they can do is transform part of a URL into something
  else.  They're very useful when translating an ID to an object in the database
  or some other similar transformation, but they won't let you change the
  response that Steinie returns.


Inspiration
-----------
Steinie was inspired in heavily by `Express`_ in the server-side JavaScript
world.  For the 4.x rewrite, Express started leaning heavily on the router based
model that Steinie uses.

.. _Express: http://expressjs.com/
.. _Werkzeug: http://werkzeug.pocoo.org/
