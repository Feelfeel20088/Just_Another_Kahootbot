from ..Kahoot_Bot.swarm import Swarm
from quart import request, jsonify
from . import app


swarmlist = []

@app.route('/swarm', methods=['POST'])
async def swarm():
    """starts a swarm"""
    # if the ints are strings there will be no crashes as we convert at createTask()
    data = await request.json
    amount = data.get('amount') # int
    gamepin = data.get('gamepin') # int 
    nickname = data.get('nickname') # str
    crash = data.get('crash') # bool
    ttl = data.get('ttl') # int

    if crash not in [True, False, None]:
        return jsonify({"error": "Invalid value for 'crash'. It must be either true or false."}), 400
    

    # infer crash is false seince None is falsy
    if not all([amount, gamepin, nickname, ttl]):
        return jsonify({"error": "Missing parameters"}), 400
    
    # Create and start the swarm
    swarm = Swarm()
    swarm.createSwarm(int(gamepin), nickname, crash, amount, ttl) # context will return instead of waiting
    



    return jsonify({"message": "Swarm created and tasks started"}), 200

@app.get("/status")
async def status():
    """Returns the status of all active swarms. also will clean up dead swarms."""
    swarm_info = []
    for swarm, index in enumerate(swarmlist):
        if swarm.getTimeRemaining() < 0:
            swarmlist.remove(swarm)
            continue
            
        swarm_info.append({
            "swarm": index,
            "time_remaining": swarm.getTimeRemaining(),
            "active_bots": len(swarm.tasks)
        })
    return {"active_swarms": swarm_info}
