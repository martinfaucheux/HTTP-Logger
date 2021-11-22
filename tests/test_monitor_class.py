import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import unittest

from http_monitor.monitor import Monitor


class MyTest(unittest.TestCase):
    def test_monitor_empty_log(self):

        buffer = io.StringIO()
        monitor = Monitor(buffer)
        monitor.start()
