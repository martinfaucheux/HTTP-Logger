import argparse
import sys

from monitor import Monitor


def cli():
    # Create the parser
    # TODO: improve comments
    arg_parser = argparse.ArgumentParser(description="Run the logger")

    arg_parser.add_argument(
        "file", nargs="?", type=argparse.FileType("r"), default=sys.stdin
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

    file_arg = parser_args.file
    Monitor(
        file_obj=file_arg,
        display_period=parser_args.period,
        max_rate=parser_args.maxrate,
        watch_window=parser_args.window,
    ).start()


if __name__ == "__main__":
    cli()
