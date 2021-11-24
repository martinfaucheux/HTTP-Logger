import unittest

from http_monitor.sliding_period import SlidingPeriod

from tests.utils import captured_output


class SlidingPeriodAlertTest(unittest.TestCase):
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

    def test_assert_no_alert_no_message(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)

        with captured_output() as (out, err):
            for _ in range(119):
                sp.add(100)
            self.assertEqual(out.getvalue().strip(), "")


class SlidingPeriodDisplayTest(unittest.TestCase):
    def test_assert_trigger_alert_message_content(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        with captured_output() as (out, err):
            for _ in range(120):
                sp.add(100)
            self.assertEqual(
                out.getvalue().strip(),
                "High traffic generated an alert - hits = 120 (1.00 rps), triggered at 1970-01-01 00:01:40",
            )

    def test_assert_recover_alert_message_content(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        for _ in range(120):
            sp.add(100)

        with captured_output() as (out, err):
            sp.add(241)
            self.assertEqual(
                out.getvalue().strip(),
                "Traffic went back to normal at 1970-01-01 00:01:40",
            )

    def test_assert_no_duplicate_message_long_event(self):

        sp = SlidingPeriod(time_window=120, max_rate=1)
        with captured_output() as (out, err):
            for _ in range(240):
                sp.add(100)
            self.assertEqual(
                out.getvalue().strip(),
                "High traffic generated an alert - hits = 120 (1.00 rps), triggered at 1970-01-01 00:01:40",
            )
