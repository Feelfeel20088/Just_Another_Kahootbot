from pydantic import BaseModel
from .bases import MetaConnect, Ext

class Advice(BaseModel):
    interval: int
    timeout: int
    reconnect: str

class MetaConnectEvent(MetaConnect):
    channel: str = "/meta/connect"
    ext: Ext
    advice: Advice
    id: str
    successful: bool

    async def handle(self, instance):
        pass
