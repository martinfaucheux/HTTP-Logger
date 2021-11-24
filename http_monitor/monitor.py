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
        """
        Object reponsible of reading lines of file and feeding them to Period objects

        Args:
            file_obj (IOBase): file object containing the http logs
            display_period (int, optional): stats will be displayed for each of these periods. Defaults to 10.
            max_rate (int, optional): request rate above which an alert will be triggered. Defaults to 10.
            watch_window (int, optional): window used to compute the current rate. Defaults to 120.
        """
        self.file_obj = file_obj
        self.ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")
        self.current_period = RecurrentPeriod(time_window=display_period)
        self.sliding_period = SlidingPeriod(time_window=watch_window, max_rate=max_rate)

    def start(self) -> None:
        """
        Start reading the file lines
        """
        csvreader = csv.reader(self.file_obj)

        for row in csvreader:
            if self.is_valid_line(row):
                (_, _, _, str_date, request, _, _) = row

                date = int(str_date)
                section = self.get_section(request)

                self.current_period.add(date, section)
                self.sliding_period.add(date)

    def is_valid_line(self, line: List[str]) -> bool:
        """
        check that the csv line read can be interpreted as http request

        Args:
            line (List[str]): csv line to be checked

        Returns:
            bool: whether it is valid or not
        """
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

        Args:
            request (str): string containing the request information

        Returns:
            str: section of the full route identified in the request
        """
        route = request.split(" ")[1]
        return "/" + route[1:].split("/", 1)[0]
