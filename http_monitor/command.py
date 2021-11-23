import argparse
import sys

from http_monitor.monitor import Monitor


def cli():
    arg_parser = argparse.ArgumentParser(description="Run http log monitoring tool")

    arg_parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="csv file to read the http log from",
    )

    arg_parser.add_argument(
        "-r",
        "--maxrate",
        type=int,
        default=10,
        help="Maximum rate (requests per second) above which an alert will be triggered",
    )

    arg_parser.add_argument(
        "-w",
        "--window",
        type=int,
        default=120,
        help="Time window (in seconds) to compute average requests per second. Default is set to 120",
    )

    arg_parser.add_argument(
        "-p",
        "--period",
        type=int,
        default=10,
        help="Display traffic for each interval of this period (in seconds). Default is 10.",
    )

    parser_args = arg_parser.parse_args(sys.argv[1:])

    Monitor(
        file_obj=parser_args.file,
        display_period=parser_args.period,
        max_rate=parser_args.maxrate,
        watch_window=parser_args.window,
    ).start()
