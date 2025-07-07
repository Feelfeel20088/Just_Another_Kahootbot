from pydantic import BaseModel, model_validator
from typing import Any, Dict, List, Optional
from .bases import ServicePlayer, Ext
import orjson



class Content(BaseModel):
    playerName: Optional[str] = None
    hostPrimaryUsage: Optional[str] = None
    hostPrimaryUsageType: Optional[str] = None
    hostIsPublisher: Optional[bool] = None
    enableBasicPostGameSignupFlow: Optional[bool] = None
    trainingContentId: Optional[str] = None
    iosLiveActivityId: Optional[str] = None
    youtubeAPIKey: Optional[str] = None


class Data(BaseModel):
    gameid: str
    host: str
    id: int
    type: str
    content: Content  
    cid: str
    trainingContentId: Optional[str] = None
    hostPrimaryUsage: Optional[str] = None
    hostPrimaryUsageType: Optional[str] = None
    youtubeAPIKey: Optional[str] = None
    iosLiveActivityId: Optional[str] = None
    playerName: Optional[str] = None
    enableBasicPostGameSignupFlow: Optional[bool] = None
    hostIsPublisher: Optional[bool] = None


class ServicePlayerEventV3(ServicePlayer):
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