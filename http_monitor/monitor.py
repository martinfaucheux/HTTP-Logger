import csv
import re
from io import IOBase
from typing import List

from http_monitor.recurrent_period import RecurrentPeriod
from http_monitor.sliding_period import SlidingPeriod


class Monitor:
    def __init__(
        self,
        file_obj: IOBase,
        display_period: int = 10,
        max_rate: int = 10,
        watch_window: int = 120,
    ) -> None:
        self.file_obj = file_obj
        self.period_length = display_period

        self.ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

        self.current_period = RecurrentPeriod(time_window=display_period)
        self.sliding_period = SlidingPeriod(time_window=watch_window, max_rate=max_rate)

    def start(self) -> None:

        csvreader = csv.reader(self.file_obj)

        for row in csvreader:
            if self.is_valid_line(row):
                remotehost, rfc931, authuser, date, request, status, bytes_count = row

                # TODO: check type first
                date = int(date)

                if not self.current_period.is_included(date):
                    self.current_period.print_report()
                    self.current_period = RecurrentPeriod(time_window=self.period_length)

                section = self.get_section(request)
                self.current_period.add(date, section)
                self.sliding_period.add(date)

    def is_valid_line(self, line: List[str]) -> bool:
        """only check if first element is an IP address"""
        return self.ip_pattern.match(line[0])

    @staticmethod
    def get_section(request: str) -> str:
        route = request.split(" ")[1]
        return "/" + route[1:].split("/", 1)[0]
