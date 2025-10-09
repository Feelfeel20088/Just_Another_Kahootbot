from justAnotherKahootBot.kahootBot.swarm import Swarm
from quart import request, jsonify
from . import app
from .context import Context 


context = Context()

@app.route('/swarm/killSwarm', methods=['POST'])
async def killSwarm():
    """Kills a swarm"""
    data = await request.json
    
    id = data.get('id') 

    swarm = context.getSwarm(id)

    swarm.killSwarm(None)
    
    return jsonify({"message": "Swarm killed"}), 200

