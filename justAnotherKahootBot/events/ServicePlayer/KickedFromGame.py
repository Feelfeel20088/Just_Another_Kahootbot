from pydantic import BaseModel, model_validator
from .bases import ServicePlayer, Ext
import orjson
from ...Kahoot_Bot.exceptions import KickedFromGameError, TooManyPlayersError
from ....config.logger import logger

class Content(BaseModel):
    kickCode: int

class Data(BaseModel):
    gameid: str
    host: str
    id: int
    type: str
    content: Content
    cid: str

class KickedFromGame(ServicePlayer):
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
        if self.data.content.kickCode == 1:
            raise KickedFromGameError("Host kicked bot from game, rejoining...")

        if self.data.content.kickCode == 2:
            raise TooManyPlayersError("Bot could not join game as the player limit has been reached.")
        
        logger.warning(f"got unknown kickcode in {type(KickedFromGame)} code: {self.data.content.kickCode}")


