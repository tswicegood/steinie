import random
from unittest import TestCase

import mock
import werkzeug

from steinie import app
from steinie import routing

from . import utils


def generate_example_environ(method="GET"):
    return {
        'HTTP_HOST': 'example.com',
        'PATH_INFO': '/',
        'REQUEST_METHOD': method,
        'wsgi.url_scheme': ('http', '80'),
    }


def generate_mock_request(environ=None):
    if environ is None:
        environ = generate_example_environ()
    return mock.Mock(path="/bar/foo", environ=environ)


class NestedRoutingTestCase(TestCase):
    def test_allows_tested_router(self):
        r1 = routing.Router()

        @r1.get("/foo")
        def handle_foo(request, response):
            return "\n".join([
                "request.path: %s" % request.path,
                "request.original_path: %s" % request.original_path,
            ])

        r2 = routing.Router()
        r2.use("/bar", r1)

        request = mock.Mock(path="/bar/foo", environ=generate_example_environ())
        response = r2.handle(request, mock.Mock())
        expected = "\n".join([
            "request.path: /foo",
            "request.original_path: /bar/foo",
        ])
        self.assertEqual(expected, response)

    def test_middleware_is_instaniated_with_route(self):
        Middleware = mock.Mock()
        r = routing.Router()
        r.use(Middleware)

        @r.get("/foo")
        def handler(*args):
            pass

        a = app.Steinie()
        a.use("/bar", r)

        a.handle(generate_mock_request(), mock.Mock())
        Middleware.assert_called_once_with(r)


class ParamFunctionTestCase(TestCase):
    def test_basic_router(self):
        num = random.randint(1000, 2000)
        router = routing.Router()
        expected = "foo{}".format(random.randint(100, 200))

        call_count = []

        @router.param("bar")
        def bar_to_upper(param):
            return param.upper()

        @router.get("/<bar:baz>/")
        def parameter(request):
            call_count.append(num)
            self.assertIn('baz', request.params)
            self.assertEqual(request.params['baz'], expected.upper())

        path = "/{0}/".format(expected)
        request = mock.Mock(path=path, environ=generate_example_environ())
        router.handle(request, mock.Mock())

        self.assert_(len(call_count) == 1)
        self.assertIn(num, call_count)

    def test_wraps_existing_func(self):
        router = routing.Router()

        @router.param("bar")
        def bar_to_upper(param):
            return param.upper()

        self.assertEqual(bar_to_upper("foo"), "FOO")
        self.assertEqual(bar_to_upper.__name__, "bar_to_upper")

    def test_supports_nested_params(self):
        num = random.randint(1000, 2000)
        router = routing.Router()
        expected = "foo{}".format(random.randint(100, 200))

        call_count = []

        @router.param("bar")
        def bar_to_upper(param):
            return param.upper()

        @router.get("/<bar:baz>/")
        def parameter(request):
            call_count.append(num)
            self.assertIn('baz', request.params)
            self.assertEqual(request.params['baz'], expected.upper())

        path = "/{0}/".format(expected)
        request = mock.Mock(path=path, environ=generate_example_environ())
        router.handle(request, mock.Mock())

        self.assert_(len(call_count) == 1)
        self.assertIn(num, call_count)

        router2 = routing.Router()
        router2.use("/", router)
        router2.handle(request, mock.Mock())

        self.assert_(len(call_count) == 2)


class DecoratedHeadFunctionsTestCase(TestCase):
    def test_wrapps_existing_func(self):
        router = routing.Router()

        @router.head("/")
        def index(request, response):
            return request.path

        random_path = "/foo/bar/%s" % random.randint(100, 200)
        request = mock.Mock(path=random_path)

        self.assertEqual(index(request, mock.Mock()), random_path)
        self.assertEqual(index.__name__, "index")

    def test_is_dispatched_to_via_handle(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.head("/")
        def index(request, response):
            return r

        post_environ = generate_example_environ(method='HEAD')
        request = mock.Mock(path='/', environ=post_environ)

        response = router.handle(request, mock.Mock())
        self.assertEqual(r, response)

    def test_does_not_match_on_get_or_post(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.head("/")
        def index(request, response):
            return r

        get_environ = generate_example_environ(method='GET')
        request = mock.Mock(path='/', environ=get_environ)

        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())

        post_environ = generate_example_environ(method='POST')
        request = mock.Mock(path='/', environ=post_environ)
        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())


class DecoratedInfoFunctionsTestCase(TestCase):
    def test_wrapps_existing_func(self):
        router = routing.Router()

        @router.info("/")
        def index(request, response):
            return request.path

        random_path = "/foo/bar/%s" % random.randint(100, 200)
        request = mock.Mock(path=random_path)

        self.assertEqual(index(request, mock.Mock()), random_path)
        self.assertEqual(index.__name__, "index")

    def test_is_dispatched_to_via_handle(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.info("/")
        def index(request, response):
            return r

        post_environ = generate_example_environ(method='INFO')
        request = mock.Mock(path='/', environ=post_environ)

        response = router.handle(request, mock.Mock())
        self.assertEqual(r, response)

    def test_does_not_match_on_get_or_post(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.info("/")
        def index(request, response):
            return r

        get_environ = generate_example_environ(method='GET')
        request = mock.Mock(path='/', environ=get_environ)

        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())

        post_environ = generate_example_environ(method='POST')
        request = mock.Mock(path='/', environ=post_environ)
        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())


class DecoratedOptionFunctionsTestCase(TestCase):
    def test_wrapps_existing_func(self):
        router = routing.Router()

        @router.options("/")
        def index(request, response):
            return request.path

        random_path = "/foo/bar/%s" % random.randint(100, 200)
        request = mock.Mock(path=random_path)

        self.assertEqual(index(request, mock.Mock()), random_path)
        self.assertEqual(index.__name__, "index")

    def test_is_dispatched_to_via_handle(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.options("/")
        def index(request, response):
            return r

        environ = generate_example_environ(method='OPTIONS')
        request = mock.Mock(path='/', environ=environ)

        response = router.handle(request, mock.Mock())
        self.assertEqual(r, response)

    def test_does_not_match_on_get_or_post(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.options("/")
        def index(request, response):
            return r

        get_environ = generate_example_environ(method='GET')
        request = mock.Mock(path='/', environ=get_environ)

        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())

        post_environ = generate_example_environ(method='POST')
        request = mock.Mock(path='/', environ=post_environ)
        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())


class DecoratedPostFunctionsTestCase(TestCase):
    def test_wraps_existing_func(self):
        router = routing.Router()

        @router.post("/")
        def index(request):
            return request.path

        random_path = "/foo/bar/%s" % random.randint(100, 200)
        request = mock.Mock(path=random_path)

        self.assertEqual(index(request), random_path)
        self.assertEqual(index.__name__, "index")

    def test_is_dispatched_to_via_handle(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.post("/")
        def index(request):
            return r

        post_environ = generate_example_environ(method='POST')
        request = mock.Mock(path='/', environ=post_environ)

        response = router.handle(request, mock.Mock())
        self.assertEqual(r, response)

    def test_does_not_match_on_get(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.post("/")
        def index(request, response):
            return r

        post_environ = generate_example_environ(method='GET')
        request = mock.Mock(path='/', environ=post_environ)

        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())


class DecoratedGetFunctionsTestCase(TestCase):
    def test_wraps_existing_func(self):
        router = routing.Router()

        @router.get("/")
        def index(request):
            return request.path

        random_path = "/foo/bar/%s" % random.randint(100, 200)
        request = mock.Mock(path=random_path)

        self.assertEqual(index(request), random_path)
        self.assertEqual(index.__name__, "index")

    def test_does_not_match_on_post(self):
        router = routing.Router()

        @router.get("/")
        def index(request):
            return request.path

        post_environ = generate_example_environ(method='POST')
        request = mock.Mock(path="/", environ=post_environ, method='POST')
        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request, mock.Mock())


class MiddlewareTestCase(TestCase):
    def test_allows_using_middleware(self):
        class Middleware(object):
            def __init__(self, app):
                pass

            def __call__(self, request, response, _next):
                response.data = "MIDDLEWARE INVOKED"
                return response

        a = app.Steinie()
        a.use(Middleware)

        with utils.run_app(a):
            response = utils.get("http://localhost:5151/baz")
            self.assertIn("MIDDLEWARE INVOKED", response.content)

    def test_allows_using_middleware_from_nested_routers(self):
        class Middleware(object):
            def __init__(self, app):
                pass

            def __call__(self, request, response, _next):
                response.data = "MIDDLEWARE INVOKED"
                return response

        r = routing.Router()
        r.use(Middleware)

        @r.get("/baz")
        def get(request):
            pass

        a = app.Steinie()
        a.use('/', r)

        with utils.run_app(a):
            response = utils.get("http://localhost:5151/baz")
            self.assertIn("MIDDLEWARE INVOKED", response.content)

    def test_dispatches_if_next_is_called(self):
        class Middleware(object):
            def __init__(self, app):
                pass

            def __call__(self, request, response, _next):
                return _next(request, response)

        a = app.Steinie()
        a.use(Middleware)

        @a.get("/foo")
        def get(request, response):
            return "Hello from the route"

        with utils.run_app(a):
            response = utils.get("http://localhost:5151/foo")
            self.assertIn("Hello from the route", response.content)

    def test_does_not_call_root_if_next_is_not_called(self):
        class Middleware(object):
            def __init__(self, app):
                pass

            def __call__(self, request, response, _next):
                pass

        a = app.Steinie()
        a.use(Middleware)

        @a.get("/foo")
        def get(request, response):
            return "Should never see this"

        with utils.run_app(a):
            response = utils.get("http://localhost:5151/foo")
            self.assertEqual('', response.content)
