import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def captured_output():
    """
    Capture output of stdout and stderr and store it in StringIO object
    This allows to test the output on standard output
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def prepare_buffer(csv_data=None):
    """
    helper to prepare buffer and add optional data for tests
    """
    buffer = StringIO()
    if csv_data is not None:
        buffer.write(csv_data)
        buffer.seek(0)
    return buffer
