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


class wrap_all_funcs_TestCase(unittest.TestCase):
    def test_wraps_list_of_functions(self):
        global call_count
        call_count = 0

        def first(_next):
            global call_count
            call_count += 1
            self.assertEqual(call_count, 1)
            _next()

        def second(_next):
            global call_count
            call_count += 1
            self.assertEqual(call_count, 2)
            _next()

        def third():
            global call_count
            call_count += 1
            self.assertEqual(call_count, 3)

        wrapped = utils.wrap_all_funcs(first, second, third)
        wrapped()
        self.assertEqual(call_count, 3)
