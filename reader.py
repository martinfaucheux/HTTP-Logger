import csv
import re
from collections import defaultdict
from datetime import datetime
from io import IOBase
from typing import Optional


class Monitor:
    def __init__(
        self,
        file_obj,
        display_period: int = 10,
        max_rate: int = 10,
        watch_window: int = 120,
    ) -> None:
        self.file_obj = file_obj
        self.period_length = display_period

        self.ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

        self.current_period: Optional[Period] = None
        self.sliding_period = SlidingPeriod(time_window=watch_window, max_rate=max_rate)

    def start(self) -> None:

        csvreader = csv.reader(self.file_obj)

        for row in csvreader:
            if self.is_valid_line(row):
                remotehost, rfc931, authuser, date, request, status, bytes_count = row

                # TODO: check type first
                date = int(date)

                if self.current_period is None:
                    self.current_period = Period(date, length=self.period_length)

                elif not self.current_period.is_included(date):
                    self.current_period.print_report()
                    self.current_period = Period(date, length=self.period_length)

                section = self.get_section(request)
                self.current_period.add(section)
                self.sliding_period.add(date)

    def is_valid_line(self, line: list[str]) -> bool:
        """only check if first element is an IP address"""
        return self.ip_pattern.match(line[0])

    @staticmethod
    def get_section(request: str) -> str:
        route = request.split(" ")[1]
        return "/" + route[1:].split("/", 1)[0]


class Period:
    def __init__(self, start_date: int, length: int = 10) -> None:
        self.start_date = start_date
        self.length = length
        self.request_count: int = 0

        self.hits = defaultdict(int)

    def add(self, section: str) -> None:
        self.hits[section] += 1
        self.request_count += 1

    def print_report(self) -> None:
        most_hit = max(self.hits, key=self.hits.get)
        hit_count = self.hits[most_hit]
        percent = round(100 * hit_count / self.request_count, 2)
        print(f"most hit: {most_hit} {hit_count} ({percent}%)")

    def is_included(self, date: int) -> bool:
        return date < self.start_date + self.length


class SlidingPeriod:
    def __init__(self, time_window=120, max_rate=10):
        self.time_window = time_window
        self.max_rate = max_rate
        self.is_alert: bool = False
        self.watched_count = 0

        self.watched_requests: list[int] = []

    def add(self, date: int) -> None:
        index = 0
        for watched_date in self.watched_requests:
            if watched_date > date - self.time_window:
                break
            index += 1

        self.watched_requests = self.watched_requests[index:] + [date]
        self.watched_count += 1 - index

        self.check_warning(date)

    def check_warning(self, date: int) -> None:

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
        return self.watched_count / self.time_window
