from quart import Quart
# TODO make a actual api not ts
app = Quart(__name__)

# init it 
from . import createSwarm
from . import status
from . import killSwarm