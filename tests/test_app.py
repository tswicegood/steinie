import random
import socket
import unittest

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
