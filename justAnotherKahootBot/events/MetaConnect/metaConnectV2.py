from .bases import MetaConnect
from typing import Optional
from pydantic import BaseModel

class Advice(BaseModel):
    interval: int
    timeout: int
    reconnect: str

class Ext(BaseModel):
    ack: int

class MetaConnectV1(MetaConnect):
    ext: Ext
    channel: str = '/meta/connect'
    id: str
    successful: bool
    advice: Advice
    
    async def handle(self, instance):
        pass