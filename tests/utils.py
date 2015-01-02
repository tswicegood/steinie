from contextlib import contextmanager


@contextmanager
def terminate_process(process):
    try:
        yield
    finally:
        if process.is_alive():
            process.terminate()
