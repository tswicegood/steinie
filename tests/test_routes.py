import random
from unittest import TestCase

import mock

from steinie import exceptions
from steinie import routes


def generate_example_environ(method="GET"):
    return {
        'HTTP_HOST': 'example.com',
        'PATH_INFO': '/',
        'REQUEST_METHOD': method,
        'wsgi.url_scheme': ('http', '80'),
    }


class ParamFunctionTestCase(TestCase):
    def test_basic_router(self):
        num = random.randint(1000, 2000)
        router = routes.Router()
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
        request = mock.Mock(path=path, environ=generate_example_environ(), method='GET')
        r = router.handle(request)
        r()

        self.assert_(len(call_count) == 1)
        self.assertIn(num, call_count)

    def test_wraps_existing_func(self):
        router = routes.Router()

        @router.param("bar")
        def bar_to_upper(param):
            return param.upper()

        self.assertEqual(bar_to_upper("foo"), "FOO")
        self.assertEqual(bar_to_upper.__name__, "bar_to_upper")


class DecoratedGetFunctionsTestCase(TestCase):
    def test_wraps_existing_func(self):
        router = routes.Router()

        @router.get("/")
        def index(request):
            return request.path

        random_path = "/foo/bar/%s" % random.randint(100, 200)
        request = mock.Mock(path=random_path)

        self.assertEqual(index(request), random_path)
        self.assertEqual(index.__name__, "index")

    def test_does_not_match_on_post(self):
        router = routes.Router()

        @router.get("/")
        def index(request):
            return request.path

        post_environ = generate_example_environ(method='POST')
        request = mock.Mock(path="/", environ=post_environ, method='POST')
        with self.assertRaises(exceptions.Http405):
            router.handle(request)()
