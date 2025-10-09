from quart import Quart
import asyncio
# TODO make a actual api not ts
app = Quart(__name__)

from .context import Context

context = Context()
watchdog_task = None 

@app.before_serving
async def startup():
    global watchdog_task
    # now the event loop is running
    watchdog_task = asyncio.create_task(context.watchdog())

@app.after_serving
async def shutdown():
    if watchdog_task:
        watchdog_task.cancel()
        try:
            await watchdog_task
        except asyncio.CancelledError:
            pass

# init it 
from . import createSwarm
from . import status
from . import killSwarm