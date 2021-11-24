from datetime import datetime
from typing import List, Optional


class SlidingPeriod:
    def __init__(self, time_window: int = 120, max_rate: int = 10):
        """
        Data structure which store the dates of the last request within the specified time window.
        When adding an element, this will display an alert if
        the mean rate is above specified level

        Args:
            time_window (int, optional): used to compute the mean request per seconds. Defaults to 120.
            max_rate (int, optional): number of request per seconds to update the alert status. Defaults to 10.
        """
        self.time_window = time_window
        self.max_rate = max_rate
        self.is_alert: bool = False
        self.watched_count = 0
        self.last_date: Optional[int]  # last date added

        self.watched_requests: List[int] = []

    def add(self, date: int) -> None:
        """
        Add a date to the period. This will
        - remove the dates exceed the specified window
        - trigger an alert if the mean rate is above specified level

        Args:
            date (int): unix timestamp to be added in the period
        """
        index = 0
        for watched_date in self.watched_requests:
            if watched_date > date - self.time_window:
                break
            index += 1

        self.watched_requests = self.watched_requests[index:] + [date]
        self.watched_count += 1 - index

        self.check_warning(date)
        self.last_date = date

    def check_warning(self, date: int) -> None:
        """
        update the alert status and display a message if the alert is trigger
        or recovered

        Arts:
            date (int): unix timestamp that should show in the warning message
        """
        is_above_limit = self.current_rate >= self.max_rate

        if is_above_limit and not self.is_alert:
            self.is_alert = True
            date_obj = datetime.utcfromtimestamp(date)
            print(
                f"High traffic generated an alert - hits = {self.watched_count} "
                f"({self.current_rate:.2f} rps), triggered at {date_obj}"
            )

        elif not is_above_limit and self.is_alert:
            self.is_alert = False
            date_obj = datetime.utcfromtimestamp(self.last_date)
            print(f"Traffic went back to normal at {date_obj}")

    @property
    def current_rate(self) -> float:
        """
        return the current number of request per seconds (mean within time window)
        """
        return self.watched_count / self.time_window
