import random
from unittest import TestCase

import mock

from steinie import routes


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

        url = "/{0}/".format(expected)
        request = mock.Mock(url=url)
        r = router.find_for(request)
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
