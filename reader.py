import csv
import re
from io import IOBase
from typing import Optional


class Monitor:
    def __init__(self, file_obj, warning_threshold: int = 10, period: int = 10) -> None:
        self.file_obj = file_obj
        self.period = period
        self.warning_threshold = warning_threshold

        self.start_time: Optional[int] = None
        self.period_start_time: Optional[int] = None
        self.period_request_count: int = 0
        self.total_request_count: int = 0

        self.ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

        self.is_alert: bool = False

    def start(self) -> None:

        csvreader = csv.reader(self.file_obj)

        for row in csvreader:
            if self.is_valid_line(row):
                print(row)
                remotehost, rfc931, authuser, date, request, status, bytes_count = row

                # TODO: check type first
                date = int(date)

                if self.start_time is None or not self.is_in_period(date):
                    self.start_new_period(date)

                self.total_request_count += 1
                self.period_request_count += 1

                if (
                    not self.is_alert
                    and self.period_request_count > self.warning_threshold
                ):
                    print("WARNING !!!")
                    self.is_alert = True

    def is_in_period(self, date: int) -> bool:
        return date - self.period_start_time < self.period

    def start_new_period(self, date: int) -> None:
        if self.start_time is None:
            self.start_time = date

        self.period_start_time = date
        self.period_request_count = 0
        print("NEW PERIOD")

    def is_valid_line(self, line: list[str]):
        """only check if first element is an IP address"""
        return self.ip_pattern.match(line[0])
