import argparse
from justAnotherKahootBot.config.state import set_args
import os

# get command line inputs here.
# this should be simple stuff like bindings to where the config file is.
# the config file should hold more important config but some command line 
# arguments can be kept to overide the config.


parser = argparse.ArgumentParser(prog="Just Another Kahootbot (JAKBOT)", description="Just Another Kahoot Bot")

subparsers = parser.add_subparsers(dest="mode", required=True, help="Available bot modes")

serve_parser = subparsers.add_parser("serve", help="Run the bot in serve mode")
oneshot_parser = subparsers.add_parser("oneshot", help="Run the bot in oneshot mode")
host_parser = subparsers.add_parser("host", help="Run the bot in host mode")


serve_parser.add_argument("-c", "--config", type=str, default="", help="Path to the config file. If not specified config will go to /tmp/just_another_kahootbot/config.json")
serve_parser.add_argument("-a", "--address", type=str, default="0.0.0.0", help="The address the Kahoot bot will bind to")
serve_parser.add_argument("-p", "--port", type=str, default="8000", help="The port the bot will bind to") # Changed type to int

# 0: Silent
# 1: logs and fatal
# 2: logs, warning and fatal
# 3: debug mode 

parser.add_argument(
    "-v", "--verbose",
    type=int,
    choices=range(0, 4),
    help=(
        "Enable verbose logging:\n"
        "  0: Silent\n"
        "  1: Logs and fatal\n"
        "  2: Logs, warnings, and fatal\n"
        "  3: Debug mode"
    )
)

class LogDirAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        logdir = values[0] if isinstance(values, list) else values


        os.makedirs(logdir, exist_ok=True)
        
        setattr(namespace, self.dest, logdir)


parser.add_argument(
    "-l", "--log-dir",
    default="/tmp/just_another_kahoot_bot",
    action=LogDirAction,
    type=str,
    help="Path to a file to write logs. If not specified, logs go to stdout."
)

oneshot_parser.add_argument("-c", "--count", type=int, default=10, help="Number of bots to join with")
oneshot_parser.add_argument("-p", "--game-pin", type=int, required=True, help="Number of bots to join with")
oneshot_parser.add_argument("-u", "--uuid", type=str, default=10, help="Number of bots to join with")


# make hoster args when i actually build the hoster

args = parser.parse_args()
set_args(args)

from justAnotherKahootBot.events import init_events
import hypercorn.asyncio
import asyncio
import sys
from hypercorn.config import Config
from quart import Quart
from justAnotherKahootBot.api import app 
from justAnotherKahootBot.config.logger import setup_logger


def main():
    setup_logger()
    init_events()
    config = Config.from_mapping(bind=[f"{args.address}:{args.port}"])
    asyncio.run(hypercorn.asyncio.serve(app, config)) 

if __name__ == "__main__":
    main()

