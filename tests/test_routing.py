import random
from unittest import TestCase

import mock
import werkzeug

from steinie import routing


def generate_example_environ(method="GET"):
    return {
        'HTTP_HOST': 'example.com',
        'PATH_INFO': '/',
        'REQUEST_METHOD': method,
        'wsgi.url_scheme': ('http', '80'),
    }


class NestedRoutingTestCase(TestCase):
    def test_allows_tested_router(self):
        r1 = routing.Router()

        @r1.get("/foo")
        def handle_foo(request):
            return "\n".join([
                "request.path: %s" % request.path,
                "request.original_path: %s" % request.original_path,
            ])

        r2 = routing.Router()
        r2.use("/bar", r1)

        request = mock.Mock(path="/bar/foo", environ=generate_example_environ())
        response = r2.handle(request)
        expected = "\n".join([
            "request.path: /foo",
            "request.original_path: /bar/foo",
        ])
        self.assertEqual(expected, response)


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
        router.handle(request)

        self.assert_(len(call_count) == 1)
        self.assertIn(num, call_count)

    def test_wraps_existing_func(self):
        router = routing.Router()

        @router.param("bar")
        def bar_to_upper(param):
            return param.upper()

        self.assertEqual(bar_to_upper("foo"), "FOO")
        self.assertEqual(bar_to_upper.__name__, "bar_to_upper")


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

        response = router.handle(request)
        self.assertEqual(r, response)

    def test_does_not_match_on_get(self):
        r = random.randint(1000, 2000)
        router = routing.Router()

        @router.post("/")
        def index(request):
            return r

        post_environ = generate_example_environ(method='GET')
        request = mock.Mock(path='/', environ=post_environ)

        with self.assertRaises(werkzeug.exceptions.MethodNotAllowed):
            router.handle(request)


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
            router.handle(request)