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


class req_or_res_TestCase(unittest.TestCase):
    def test_passes_request_and_response_if_both_are_available(self):
        target = mock.Mock()
        request = object()
        response = object()
        utils.req_or_res(target)(request, response)
        target.assert_called_with(request, response)

    def test_returns_result_from_wrapped_func(self):
        r = random.randint(1000, 2000)
        target = mock.Mock(return_value=r)
        actual = utils.req_or_res(target)("some request", "some response")
        self.assertEqual(actual, r)

    def test_falls_back_to_request_only_if_response_not_available(self):
        r = random.randint(1000, 2000)
        target = mock.Mock()
        target.side_effect = [TypeError(), r]
        actual = utils.req_or_res(target)("some request", "some response")
        self.assertEqual(actual, r)

    def test_is_smart_enough_to_pass_other_args_as_well(self):
        r = random.randint(100, 200)

        def first(req, res, _next):
            return _next(req, res)

        second = utils.req_or_res(mock.Mock(side_effect=[TypeError(), r]))
        wrapped = utils.wrap_all_funcs(first, second)
        actual = wrapped("some request", "some response")
        self.assertEqual(actual, r)

    def test_wrapped_functions_are_given_all_the_args(self):
        request = object()
        response = object()

        def first(req, res, _next):
            return _next(req, res)

        second = mock.Mock()
        wrapped = [utils.req_or_res(f) for f in [first, second, mock.Mock()]]
        utils.wrap_all_funcs(*wrapped)(request, response)

        second.assert_called_with(request, response, _next=mock.ANY)


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
