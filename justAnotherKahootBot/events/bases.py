from pydantic import BaseModel

class Event(BaseModel):

    channel: str

    async def handle(self, instance):
        raise NotImplementedError(f"Handle not implemented for subclass {self.__class__.__name__}!")
    
class Ext(BaseModel):
    timetrack: int