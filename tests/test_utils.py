import random
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from steinie import utils


class generate_next_TestCase(unittest.TestCase):
    def test_basic_api(self):
        def simple(_next):
            _next()
        second = mock.Mock()
        func = utils.generate_next(simple, second)
        func()
        self.assertTrue(second.called)

    def test_does_not_call_second_if_next_is_not_invoked(self):
        def simple(_next):
            pass
        second = mock.Mock()
        utils.generate_next(simple, second)()
        self.assertFalse(second.called)

    def test_wrapped_function_still_looks_the_same(self):
        def simple(_next):
            pass
        second = mock.Mock()

        wrapped = utils.generate_next(simple, second)
        self.assertEqual(wrapped.__name__, simple.__name__)
