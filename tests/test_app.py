import random
import socket
import unittest

import mock
import requests

from steinie import routes
from steinie import app

from . import utils


class SteinieTest(unittest.TestCase):
    def test_is_a_route(self):
        a = app.Steinie()
        self.assertIsInstance(a, routes.Router)

    def test_can_run_and_route_requests(self):
        random_number = random.randint(1000, 2000)
        a = app.Steinie()

        @a.get("/")
        def index(request):
            return "Random number is: {}".format(random_number)

        with utils.run_app(a):
            r = utils.get("http://localhost:5151/")
            expected = "Random number is: {}".format(random_number)
            self.assertEqual(expected, r.content)

    def test_can_run_on_random_ports(self):
        random_port = random.randint(20000, 25000)
        a = app.Steinie(port=random_port)

        @a.get("/")
        def index(request):
            return "Hi, from port {}".format(random_port)

        with utils.run_app(a):
            r = utils.get("http://localhost:{}/".format(random_port))
            expected = "Hi, from port {}".format(random_port)
            self.assertEqual(expected, r.content)

    def test_can_listen_on_alternatve_addresses(self):
        host = socket.gethostname()
        a = app.Steinie(host=host)

        @a.get("/")
        def index(request):
            return "Hi, from host {}".format(host)

        with utils.run_app(a):
            r = utils.get("http://{}:5151/".format(host))
            expected = "Hi, from host {}".format(host)
            self.assertEqual(expected, r.content)

            with self.assertRaises(requests.exceptions.ConnectionError):
                utils.get("http://loclhost:5151/")

    def test_runs_with_debug_based_on_instantiation(self):
        a = app.Steinie(debug=True)
        with mock.patch.object(app.serving, 'run_simple') as run_simple:
            a.run()

        run_simple.assert_called_with(a.host, a.port, a, use_debugger=True)

    def test_defaults_to_debug_off(self):
        a = app.Steinie()
        with mock.patch.object(app.serving, 'run_simple') as run_simple:
            a.run()
        run_simple.assert_called_with(a.host, a.port, a, use_debugger=False)

    def test_allows_nested_routes(self):
        r = routes.Router()

        @r.get("/foo")
        def handle_foo(request):
            return "\n".join([
                "request.path: %s" % request.path,
                "request.original_path: %s" % request.original_path,
            ])

        a = app.Steinie()
        a.use("/bar", r)

        with utils.run_app(a):
            response = utils.get("http://localhost:5151/bar/foo")

            expected = "\n".join([
                "request.path: /foo",
                "request.original_path: /bar/foo",
            ])
            self.assertEqual(expected, response.content)
