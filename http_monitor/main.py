import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from http_monitor.command import cli

if __name__ == "__main__":
    cli()
