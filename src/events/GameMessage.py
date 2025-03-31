from typing import List
from .bases import Event, Ext
from pydantic import BaseModel, model_validator
import orjson

class UpcomingGameBlockData(BaseModel):
    type: str
    layout: str
    pointsMultiplier: int = None

class Content(BaseModel):
    extensiveMode: bool
    gameBlockCount: int
    upcomingGameBlockData: List[UpcomingGameBlockData]
    gameId: str # why are there 2 of them :(

class Data(BaseModel):
    gameid: str # over here 
    id: int
    type: str
    content: Content 

class GameMessage(Event):
    ext: Ext
    data: Data
    channel: str = "/service/player"

    @model_validator(mode='before')
    def check_required_fields(cls, values: dict) -> dict:
        content = values.get('data', {}).get('content', None)
        
        if isinstance(content, str):
            try:
                parsed_content = orjson.loads(content)
                values["data"]["content"] = Content(**parsed_content)
            except orjson.JSONDecodeError:
                raise ValueError(f"Failed to parse content as JSON: {content}")
        return values

    async def handle(self, instance):
        pass