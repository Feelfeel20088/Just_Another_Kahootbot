from pydantic import BaseModel
from .bases import ServiceStatus, Ext
from justAnotherKahootBot.kahootBot.exceptions import TooManyPlayersError
from justAnotherKahootBot.config.logger import logger
class StatusData(BaseModel):
    type: str
    status: str

class ServiceStatusEvent(ServiceStatus):
    ext: Ext
    data: StatusData
    channel: str = "/service/status"


    async def handle(self, instance):
        if self.data.status == "QUEUE": 
            logger.debug("Too many players closing bot")
            raise TooManyPlayersError("Host disconnect from game.")
        
