import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import unittest

from http_monitor.monitor import Monitor

from tests.utils import captured_output


class MyTest(unittest.TestCase):
    def test_monitor_empty_log(self):

        buffer = self._get_buffer()
        monitor = Monitor(buffer)

        with captured_output() as (out, err):
            monitor.start()
            self.assertEqual(out.getvalue().strip(), "")

    def test_monitor_one_line(self):
        buffer = self._get_buffer(
            '"10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234'
        )
        monitor = Monitor(buffer)

        with captured_output() as (out, err):
            monitor.start()
            self.assertEqual(out.getvalue().strip(), "")

    def test_monitor_two_line_20s_interval(self):
        buffer = self._get_buffer(
            '"10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234\n'
            '"10.0.0.2","-","apache",1549579000,"GET /report/4425 HTTP/1.0",200,1256'
        )
        monitor = Monitor(buffer)

        with captured_output() as (out, err):
            monitor.start()
            self.assertEqual(out.getvalue().strip(), "most hit: /api 1 (100.0%)")

    @staticmethod
    def _get_buffer(csv_data=None):
        buffer = io.StringIO()
        if csv_data is not None:
            buffer.write(csv_data)
            buffer.seek(0)
        return buffer
