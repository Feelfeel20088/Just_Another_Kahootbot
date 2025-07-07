from ..bases import Event
from pydantic import BaseModel

class MetaConnect(Event):
    pass

# diffrent Ext model becuse instead of timetrack we have 'act'
class Ext(BaseModel):
    ack: int