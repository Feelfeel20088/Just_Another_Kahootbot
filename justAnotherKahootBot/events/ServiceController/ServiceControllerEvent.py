from .bases import ServiceController, Ext
from pydantic import BaseModel

class Data(BaseModel):
    type: str
    cid: str

class ServiceControllerEvent(ServiceController):
    channel: str = "/service/controller"
    ext: Ext
    data: Data

    async def handle(self, instance):
        pass

