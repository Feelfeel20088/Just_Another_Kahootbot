from quart import Quart

app = Quart(__name__)

# init it 
from . import swarmpost
from . import status