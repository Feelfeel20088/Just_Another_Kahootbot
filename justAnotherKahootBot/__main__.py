from justAnotherKahootBot.events import init_events
import hypercorn.asyncio
import asyncio
from hypercorn.config import Config
from quart import Quart
from justAnotherKahootBot.api import app 
from justAnotherKahootBot.config.logger import logger


def main():
    init_events()
    config = Config.from_mapping(bind=["0.0.0.0:8000"])
    asyncio.run(hypercorn.asyncio.serve(app, config)) 

if __name__ == "__main__":
    main()

