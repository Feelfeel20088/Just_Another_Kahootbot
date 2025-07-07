from pydantic import BaseModel, model_validator
from .bases import ServicePlayer, Ext
import orjson

class Content(BaseModel):
    playerName: str
    hostPrimaryUsage: str
    hostPrimaryUsageType: str
    hostIsPublisher: bool
    enableBasicPostGameSignupFlow: bool
    trainingContentId: str
    iosLiveActivityId: str
    youtubeAPIKey: str

class Data(BaseModel):
    gameid: str
    host: str
    id: int
    type: str
    content: str
    cid: str

class ServicePlayerEvent(ServicePlayer):
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

