from werkzeug.serving import run_simple

from steinie.app import create_app
from steinie.sample import application


run_simple("127.0.0.1", 9999, create_app(application), use_reloader=True)
