from pydantic import BaseModel, model_validator, Field
from .bases import ServicePlayer, Ext
from typing import List, Optional, Union
import orjson
from justAnotherKahootBot.fetcher import AnswerBuilder, Fetcher
import time
from justAnotherKahootBot.config.logger import logger

class Video(BaseModel):
    startTime: int
    endTime: int
    service: str
    fullUrl: str


class ImageMetadata(BaseModel):
    id: str
    altText: str
    contentType: str
    origin: str
    externalRef: str
    resources: str
    width: int
    height: int


class Content(BaseModel):
    gameBlockIndex: int
    totalGameBlockCount: int
    extensiveMode: bool
    type: str
    timeRemaining: int
    timeAvailable: int
    numberOfAnswersAllowed: int
    currentQuestionAnswerCount: int
    video: Video
    image: str
    imageMetadata: ImageMetadata
    media: list  # Media might be empty or have null entries

   

class Data(BaseModel):
    gameid: str
    id: int
    type: str
    content: Content


class GameBlock(ServicePlayer):
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

        t = time.time()

        fetcher: Fetcher = instance.get_fetcher()

        parser = fetcher.get_parser(self.data.content.gameBlockIndex)

        answer = AnswerBuilder.from_parser(parser).build()

        await instance.push_answer(answer)
        
        elapsed = time.time() - t
        
        logger.debug(
            f"Bot '{instance.get_nickname()}' sent answer in {elapsed:.4f}s | "
            f"Choice: {self.data.content.choice} | Type: {self.data.content.type}"
        )

        

