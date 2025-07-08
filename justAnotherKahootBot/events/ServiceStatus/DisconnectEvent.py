from pydantic import BaseModel
from .bases import ServiceStatus, Ext
from justAnotherKahootBot.kahootBot.exceptions import HostDisconnectError
from justAnotherKahootBot.config.logger import logger


class Data(BaseModel):
    reason: str
    type: str
    status: str

class DisconnectEvent(ServiceStatus):
    ext: Ext
    data: Data
    channel: str = "/service/status"

    async def handle(self, instance):
        if self.data.reason == "disconnect" and self.data.status == "MISSING":
            raise HostDisconnectError("Host disconnect from game.")
        logger.warning(f"unknown value in {type(DisconnectEvent)} disconnect: {self.data.reason}, status: {self.data.status} ")
