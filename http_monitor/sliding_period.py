from datetime import datetime
from typing import List


class SlidingPeriod:
    """
    Data structure which store the dates of the last request within the specified time window.
    When adding an element, this will display an alert if
    the mean rate is above specified level
    `time_window`: used to compute the mean request per seconds
    `max_rate`: number of request per seconds to update the alert status
    """

    def __init__(self, time_window: int = 120, max_rate: int = 10):
        self.time_window = time_window
        self.max_rate = max_rate
        self.is_alert: bool = False
        self.watched_count = 0

        self.watched_requests: List[int] = []

    def add(self, date: int) -> None:
        """
        Add a date to the period. This will
        - remove the dates exceed the specified window
        - trigger an alert if the mean rate is above specified level
        `date`: date to be added in the period
        """
        index = 0
        for watched_date in self.watched_requests:
            if watched_date > date - self.time_window:
                break
            index += 1

        self.watched_requests = self.watched_requests[index:] + [date]
        self.watched_count += 1 - index

        self.check_warning(date)

    def check_warning(self, date: int) -> None:
        """
        update the alert status and display a message if the alert is trigger
        or recovered
        `date`: date that should show in the warning message
        """

        is_above_limit = self.current_rate >= self.max_rate
        date_obj = datetime.fromtimestamp(date)

        if is_above_limit and not self.is_alert:
            self.is_alert = True
            print(
                f"High traffic generated an alert - hits = {self.watched_count}, triggered at {date_obj}"
            )

        elif not is_above_limit and self.is_alert:
            self.is_alert = False
            print(f"Traffic went back to normal at {date_obj}")

    @property
    def current_rate(self) -> float:
        """
        return the current number of request per seconds (mean within time window)
        """
        # TODO: fix this in case the the run time is less than 2min
        return self.watched_count / self.time_window
