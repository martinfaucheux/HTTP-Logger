import csv
import re
from io import IOBase
from typing import List

from http_monitor.recurrent_period import RecurrentPeriod
from http_monitor.sliding_period import SlidingPeriod


class Monitor:
    """
    Object reponsible of reading lines of file and feeding them to Period objects
    `file_obj`: file object where logs should be read
    `display_period`: stats will be displayed for each of these periods
    `max_rate`: request rate above which an alert will be triggered
    `watch_window`: window used to compute the current rate
    """

    def __init__(
        self,
        file_obj: IOBase,
        display_period: int = 10,
        max_rate: int = 10,
        watch_window: int = 120,
    ) -> None:
        self.file_obj = file_obj
        self.ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")
        self.current_period = RecurrentPeriod(time_window=display_period)
        self.sliding_period = SlidingPeriod(time_window=watch_window, max_rate=max_rate)

    def start(self) -> None:
        csvreader = csv.reader(self.file_obj)

        for row in csvreader:
            if self.is_valid_line(row):
                (_, _, _, str_date, request, _, _) = row

                # TODO: check type first
                date = int(str_date)
                section = self.get_section(request)

                self.current_period.add(date, section)
                self.sliding_period.add(date)

    def is_valid_line(self, line: List[str]) -> bool:
        """check that the csv line read can be interpreted as http request"""
        if len(line) >= 5:
            ip, _, _, str_date, request = line[:5]
            return (
                self.ip_pattern.match(ip)
                and str_date.isdigit()
                and len(request.split(" ")) == 3
            )
        return False

    @staticmethod
    def get_section(request: str) -> str:
        """
        Extract the section of the request endpoint
        e.g. "GET /api/user HTTP/1.0" -> "/api"
        """
        route = request.split(" ")[1]
        return "/" + route[1:].split("/", 1)[0]
