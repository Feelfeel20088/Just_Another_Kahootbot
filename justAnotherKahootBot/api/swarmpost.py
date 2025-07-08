from justAnotherKahootBot.kahootBot.swarm import Swarm
from quart import request, jsonify
from . import app
from .context import Context 


context = Context()

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
    context.add_swarm(swarm)
    swarm.createSwarm(int(gamepin), nickname, crash, amount, ttl, context) # context will return instead of waiting
    



    return jsonify({"message": "Swarm created and tasks started"}), 200

