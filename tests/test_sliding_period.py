import unittest

from http_monitor.sliding_period import SlidingPeriod


class SlidingPeriodTest(unittest.TestCase):
    def test_sliding_period_one_date_no(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        sp.add(100)
        self.assertFalse(sp.is_alert)

    def test_sliding_period_max_request_no_trigger(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        self.assertFalse(sp.is_alert)

        for _ in range(119):
            sp.add(100)

        self.assertFalse(sp.is_alert)

    def test_sliding_period_trigger_alert(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        self.assertFalse(sp.is_alert)

        for _ in range(120):
            sp.add(100)

        self.assertTrue(sp.is_alert)

    def test_sliding_period_alert_recovered(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        self.assertFalse(sp.is_alert)

        for _ in range(120):
            sp.add(100)

        sp.add(241)
        self.assertFalse(sp.is_alert)

    def test_sliding_period_trigger_alert_twice(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        self.assertFalse(sp.is_alert)

        for _ in range(120):
            sp.add(100)

        sp.add(241)

        for _ in range(120):
            sp.add(100)

        self.assertTrue(sp.is_alert)
