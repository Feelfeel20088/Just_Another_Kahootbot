from pydantic import BaseModel, model_validator
from typing import List, Optional
from .bases import ServicePlayer, Ext
import orjson

class AvailableCollaborations(BaseModel):
    isAutoAssign: bool
    canRename: bool
    data: List
    collaborationNameLocale: str

class Content(BaseModel):
    data: dict
    stableIdentifier: str
    isHighContrast: bool
    teamMembers: List
    loginState: int
    didControllerLeave: bool
    avatarTimestamp: Optional[int] = None
    wasControllerKicked: bool
    state: int
    availableCollaborations: AvailableCollaborations
    chosenCollaborationIndex: int
    kahootLangIsRTL: bool
    canChangeAvatar: bool
    youtubeAPIKey: str
    userReactionsEnabled: bool
    islandData: Optional[dict] = None
    audienceQuestionsData: Optional[dict] = None

class Data(BaseModel):
    gameid: str
    host: str
    id: int
    type: str
    content: Content
    cid: str

class ServicePlayerEventV4(ServicePlayer):
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

