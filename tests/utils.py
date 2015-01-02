from contextlib import contextmanager
from multiprocessing import Process
from time import sleep


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
