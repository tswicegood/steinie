from contextlib import contextmanager
from multiprocessing import Process


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

    with terminate_process(process):
        yield
