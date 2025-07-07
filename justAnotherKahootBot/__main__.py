from .kahootBot.events import event_classes
import hypercorn.asyncio
import asyncio
from hypercorn.config import Config
from quart import Quart
from .kahootBot.api import app 
from .config.logger import logger

if __name__ == "__main__":
    config = Config.from_mapping(bind=["0.0.0.0:8000"])
    asyncio.run(hypercorn.asyncio.serve(app, config)) 

