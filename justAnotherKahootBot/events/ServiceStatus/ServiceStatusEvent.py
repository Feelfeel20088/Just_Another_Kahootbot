from pydantic import BaseModel
from .bases import ServiceStatus, Ext

class StatusData(BaseModel):
    type: str
    status: str

class ServiceStatusEvent(ServiceStatus):
    ext: Ext
    data: StatusData
    channel: str = "/service/status"


    async def handle(self, instance):
        pass
