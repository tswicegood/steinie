from contextlib import contextmanager
from multiprocessing import Process
from time import sleep

import requests


def get(*args, **kwargs):
    if not 'timeout' in kwargs:
        # Fix issue where requests.get() hangs on local resolved host name
        kwargs['timeout'] = 0.1
    return requests.get(*args, **kwargs)


@contextmanager
def terminate_process(process):
    try:
        yield
    finally:
        if process.is_alive():
            process.terminate()


@contextmanager
def run_app(app):
    process = Process(target=app.run)
    process.start()

    # give this a slight second to start
    sleep(0.01)

    with terminate_process(process):
        yield
