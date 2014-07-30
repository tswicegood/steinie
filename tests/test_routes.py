import random
from unittest import TestCase

import mock

from steinie import routes


class ParamFunctionTestCase(TestCase):
    def test_basic_router(self):
        router = routes.Router()
        expected = "foo{}".format(random.randint(100, 200))

        call_count = []

        @router.param("bar")
        def bar_to_upper(param):
            return param.upper()

        @router.get("/<bar:baz>/")
        def parameter(request):
            call_count.append(1)
            self.assert_('baz' in request.params)
            self.assert_(request.params['baz'] == expected.upper())

        url = "/{0}/".format(expected)
        request = mock.Mock(url=url)
        r = router.find_for(request)
        r()

        self.assert_(len(call_count) == 1)
