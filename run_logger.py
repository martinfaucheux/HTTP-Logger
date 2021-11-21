import argparse
import sys

from reader import Monitor

if __name__ == "__main__":

    # Create the parser
    # TODO: improve comments
    arg_parser = argparse.ArgumentParser(description="Run the logger")

    arg_parser.add_argument(
        "file", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )

    parser_args = arg_parser.parse_args(sys.argv[1:])
    file_arg = parser_args.file

    Monitor(file_arg).start()
