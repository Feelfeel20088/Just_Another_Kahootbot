from pydantic import BaseModel, model_validator
from typing import Optional, List, Dict, Any
from .bases import ServicePlayer, Ext
import orjson

class AvailableCollaborations(BaseModel):
    isAutoAssign: bool
    canRename: bool
    data: List[Any]
    collaborationNameLocale: str


class Content(BaseModel):
    data: Dict[str, Any]
    stableIdentifier: str
    isHighContrast: bool
    teamMembers: List[Any]
    loginState: int
    didControllerLeave: bool
    avatarTimestamp: Optional[Any]
    wasControllerKicked: bool
    state: int
    availableCollaborations: AvailableCollaborations
    chosenCollaborationIndex: int
    kahootLangIsRTL: bool
    canChangeAvatar: bool
    youtubeAPIKey: str
    shouldBlockYouTube: bool
    userReactionsEnabled: bool
    islandData: Optional[Any]
    audienceQuestionsData: Optional[Any]


class Data(BaseModel):
    gameid: str
    host: str
    id: int
    type: str
    content: Content
    cid: str


class ServicePlayerEventV5(ServicePlayer):
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

