import unittest

from http_monitor.monitor import Monitor

from tests.utils import captured_output, prepare_buffer

DATA_DIR = "tests/data/"


class MonitorDisplayTest(unittest.TestCase):
    def test_monitor_empty_log(self):

        buffer = prepare_buffer()
        monitor = Monitor(buffer)

        with captured_output() as (out, err):
            monitor.start()
            self.assertEqual(out.getvalue().strip(), "")

    def test_monitor_one_line(self):
        buffer = prepare_buffer(
            '"10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234'
        )
        monitor = Monitor(buffer)

        with captured_output() as (out, err):
            monitor.start()
            self.assertEqual(out.getvalue().strip(), "")

    def test_monitor_several_lines(self):

        with open(DATA_DIR + "expected_output.txt") as fileobj:
            expected_message = fileobj.read()

        with open(DATA_DIR + "sample_log.txt") as fileobj:
            with captured_output() as (out, err):
                monitor = Monitor(
                    fileobj, display_period=10, watch_window=10, max_rate=1
                )
                monitor.start()
                displayed_message = out.getvalue().strip()

        self.assertEqual(displayed_message, expected_message)
