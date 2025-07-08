from justAnotherKahootBot.kahootBot.swarm import Swarm
from quart import request, jsonify
from . import app
from .context import Context 


context = Context()

@app.get("/status")
async def status():
    """Returns the status of all active swarms. also will clean up dead swarms."""
    swarm_info = []
    for swarm, index in enumerate(context.get_swarm_list()):
            
        swarm_info.append({
            "swarm": index,
            "time_remaining": swarm.getTimeRemaining(),
            "active_bots": len(swarm.tasks)
        })
    return {"active_swarms": swarm_info}
