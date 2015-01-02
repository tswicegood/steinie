import random
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
            r = requests.get("http://localhost:5151/")
            expected = "Random number is: {}".format(random_number)
            self.assertEqual(expected, r.content)
