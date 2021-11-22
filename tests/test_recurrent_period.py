import unittest

from http_monitor.recurrent_period import RecurrentPeriod

from tests.utils import captured_output


class SlidingPeriodTestDict(unittest.TestCase):
    def test_one_elt_hit_dict_content(self):
        rp = RecurrentPeriod(time_window=10)
        rp.add(100, "/report")
        self.assertDictEqual(dict(rp.hits), {"/report": 1})

    def test_two_elt_hit_dict_content(self):
        rp = RecurrentPeriod(time_window=100)
        rp.add(100, "/report")
        rp.add(101, "/report")
        self.assertDictEqual(dict(rp.hits), {"/report": 2})

    def test_several_elt_hit_dict_content(self):
        rp = RecurrentPeriod(time_window=100)
        rp.add(100, "/report")
        rp.add(101, "/report")
        rp.add(101, "/api")
        self.assertDictEqual(dict(rp.hits), {"/report": 2, "/api": 1})

    def test_hit_dict_content_after_reset(self):
        rp = RecurrentPeriod(time_window=100)
        rp.add(100, "/report")
        rp.add(101, "/api")
        rp.add(1001, "/report")
        self.assertDictEqual(dict(rp.hits), {"/report": 1})


class SlidingPeriodTestDisplay(unittest.TestCase):
    def test_empty_period_no_display(self):
        with captured_output() as (out, err):
            rp = RecurrentPeriod(time_window=10)
            self.assertEqual(out.getvalue().strip(), "")

    def test_one_elt_period_no_display(self):
        rp = RecurrentPeriod(time_window=10)
        with captured_output() as (out, err):
            rp.add(100, "/report")
            self.assertEqual(out.getvalue().strip(), "")

    def test_smaller_period_no_display(self):
        rp = RecurrentPeriod(time_window=10)
        with captured_output() as (out, err):
            rp.add(1, "/report")
            rp.add(10, "/report")
            self.assertEqual(out.getvalue().strip(), "")

    def test_refresh_period_display(self):
        rp = RecurrentPeriod(time_window=10)
        with captured_output() as (out, err):
            rp.add(1, "/report")
            rp.add(12, "/report")
            self.assertEqual(out.getvalue().strip(), "most hit: /report 1 (100.0%)")
