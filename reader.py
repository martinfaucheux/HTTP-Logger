import csv
import re
from collections import defaultdict
from io import IOBase
from typing import Optional


class Monitor:
    def __init__(
        self, file_obj, warning_threshold: int = 10, period_length: int = 10
    ) -> None:
        self.file_obj = file_obj
        self.period_length = period_length
        self.warning_threshold = warning_threshold

        self.start_time: Optional[int] = None
        self.period_start_time: Optional[int] = None
        self.period_request_count: int = 0
        self.total_request_count: int = 0

        self.ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

        self.alert_start: Optional[int] = None

        self.current_period: Optional[Period] = None

    def start(self) -> None:

        csvreader = csv.reader(self.file_obj)

        for row in csvreader:
            if self.is_valid_line(row):
                # print(row)
                remotehost, rfc931, authuser, date, request, status, bytes_count = row

                # TODO: check type first
                date = int(date)

                if self.current_period is None:
                    self.current_period = Period(date, length=self.period_length)

                elif not self.current_period.is_included(date):
                    self.current_period.print_report()
                    self.current_period = Period(date, length=self.period_length)

                self.current_period.add(request)

    def is_valid_line(self, line: list[str]):
        """only check if first element is an IP address"""
        return self.ip_pattern.match(line[0])


class Period:
    def __init__(self, start_date: int, length: int = 10) -> None:
        self.start_date = start_date
        self.length = length
        self.request_count: int = 0

        self.hits = defaultdict(int)

    def add(self, request: str):
        section = self.get_section(request)
        self.hits[section] += 1
        self.request_count += 1

    def print_report(self):
        most_hit = max(self.hits, key=self.hits.get)
        hit_count = self.hits[most_hit]
        percent = round(100 * hit_count / self.request_count, 2)

        print(f"most hit: {most_hit} {hit_count} ({percent}%)")

    def get_section(self, request: str):
        route = request.split(" ")[1]
        return "/" + route[1:].split("/", 1)[0]

    def is_included(self, date: int) -> bool:
        return date < self.start_date + self.length
