from collections import defaultdict
from typing import Optional


class RecurrentPeriod:
    """
    Data structure which store request counts within the specified time window.
    If a date exceeds the current start date, this will empty the counts and start from 0
    when this appens, this will display the section with the most hit, number of requests and the time of current request
    `time_window`: time period to gather count and display information
    """

    def __init__(self, time_window: int = 10) -> None:
        self.start_date: Optional[int] = None
        self.time_window = time_window
        self.request_count: int = 0
        self.hits = defaultdict(int)

    def add(self, date: int, section: str) -> None:
        if self.start_date is None:
            self.start_date = date

        self.hits[section] += 1
        self.request_count += 1

    def reset(self, date: int) -> None:
        self.start_date = date
        self.request_count = 0
        self.hits = defaultdict(int)

    def print_report(self) -> None:
        most_hit = max(self.hits, key=self.hits.get)
        hit_count = self.hits[most_hit]
        percent = round(100 * hit_count / self.request_count, 2)
        print(f"most hit: {most_hit} {hit_count} ({percent}%)")

    def is_included(self, date: int) -> bool:
        return self.start_date is None or date < self.start_date + self.time_window