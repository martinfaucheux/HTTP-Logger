import io
import unittest

from http_monitor.monitor import Monitor


class MonitorTest(unittest.TestCase):
    def test_is_valid_line_valid_line(self):
        line = [
            "10.0.0.2",
            "-",
            "apache",
            "1549573860",
            "GET /api/user HTTP/1.0",
            200,
            1234,
        ]
        monitor = Monitor(io.StringIO())
        self.assertTrue(monitor.is_valid_line(line))

    def test_is_valid_line_invalid_line(self):
        line = [
            "not an ip",
            "-",
            "apache",
            "1549573860",
            "GET /api/user HTTP/1.0",
            200,
            1234,
        ]
        monitor = Monitor(io.StringIO())
        self.assertFalse(monitor.is_valid_line(line))

    def test_get_section_no_subsection(self):
        monitor = Monitor(io.StringIO())
        request_string = "GET /report HTTP/1.0"
        self.assertEqual(monitor.get_section(request_string), "/report")

    def test_get_section_with_subsection(self):
        monitor = Monitor(io.StringIO())
        request_string = "GET /report/48/full HTTP/1.0"
        self.assertEqual(monitor.get_section(request_string), "/report")
