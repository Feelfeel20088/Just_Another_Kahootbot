from justAnotherKahootBot.events import init_events
import hypercorn.asyncio
import asyncio
import sys
from hypercorn.config import Config
from quart import Quart
from justAnotherKahootBot.api import app 
from justAnotherKahootBot.config.logger import logger
import argparse

# get command line inputs here.
# this should be simple stuff like bindings to where the config file is.
# the config file should hold more important config but some command line 
# arguments can be kept to overide the config.

parser = argparse.ArgumentParser(prog="Just Another Kahootbot (JAKBOT)", description="Just Another Kahoot Bot")


subparsers = parser.add_subparsers(dest="mode", required=True, help="Available bot modes")

host_parser = subparsers.add_parser("serve", help="Run the bot in host mode.")
parser.add_argument("-c", "--config", type=str, default="", help="Path to the config file. If not specified config will go to /tmp/just_another_kahootbot/config.json")
parser.add_argument("-a", "--address", type=str, default="0.0.0.0", help="The address the Kahoot bot will bind to")
parser.add_argument("-p", "--port", type=str, default="8000", help="The port the bot will bind to") # Changed type to int

# 0: Silent
# 1: logs and fatal
# 2: logs, warning and fatal
# 3: debug mode 
parser.add_argument("-v", "--verbose", type=int, help="Enable verbose logging") 

parser.add_argument("--log-file", type=str, help="Path to a file to write logs. If not specified, logs go to stdout.")


serve_parser = subparsers.add_parser("oneshot", help="Run the bot in host mode.")
serve_parser.add_argument("-c", "--count", type=int, default=10, help="Number of bots to join with")
serve_parser.add_argument("-p", "--game-pin", type=int, required=True, help="Number of bots to join with")
serve_parser.add_argument("-u", "--uuid", type=str, default=10, help="Number of bots to join with")


serve_parser = subparsers.add_parser("host", help="Run the bot in serve mode.")
serve_parser.add_argument("game_pin", type=int, help="The game PIN to join")


args = parser.parse_args()


def main():
    init_events()
    config = Config.from_mapping(bind=[f"{args.address}:{args.port}"])
    asyncio.run(hypercorn.asyncio.serve(app, config)) 

if __name__ == "__main__":
    main()

