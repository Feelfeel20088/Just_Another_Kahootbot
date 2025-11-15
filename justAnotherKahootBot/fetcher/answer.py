from justAnotherKahootBot.kahootBot.client_info import ClientInfo
from justAnotherKahootBot.kahootBot.payloads import Payloads
from pydantic import BaseModel
from typing import Optional, Dict, Any
import orjson
from justAnotherKahootBot.config.logger import logger
import time
import random
from .parse import BaseQuestionParser 

class Content(BaseModel):
    type: str
    choice: int
    questionIndex: int


class DataPayload(BaseModel):
    gameid: str
    type: str
    host: str
    id: int
    content: str  # JSON stringified Content model


class Answer(BaseModel):
    id: str
    channel: str
    data: DataPayload
    clientId: str
    ext: Dict[str, Any]

    
    async def send_answer(self, ws, id, act):
        """Send a built Kahoot answer through the websocket."""
        
        await self.__generic_heartbeat(ws, id, act)

        await ws.send(orjson.dumps(self.model_dump()).decode())

    @classmethod
    async def __generic_heartbeat(cls, ws, id: int, act: int):

        await ws.send(Payloads.__heartBeat__(id, act))




# {
#     "id": str(id),
#     "channel": "/service/controller",
#     "data": {
#         "gameid":self.gameid,
#         "type": "message",
#         "host": "kahoot.it",
#         "id": 45, 
#         "content": json.dumps({
#         "type": type,
#         "choice":random.randint(0,3),
#         "questionIndex":self.questionIndex
#         })
#     },
#     "clientId": self.clientid,
#     "ext": {}
# }

class AnswerBuilder:
    def __init__(self, client_info: ClientInfo):
        self._client_info = client_info
        self._type: Optional[str] = None
        self._choice: Optional[int] = None
        self._parser: Optional[BaseQuestionParser] = None

    # Manual setters
    def set_type(self, question_type: str):
        self._type = question_type
        return self

    def set_choice(self, choice: int):
        self._choice = choice
        return self

    def set_question_index(self, index: int):
        self._question_index = index
        return self

    def from_parser(self, parser: BaseQuestionParser, choice_strategy: str = "correct"):
        """
        Fill fields automatically from a parser instance.
        choice_strategy: "correct", "incorrect", "random"
        """
        self._parser = parser
        self._type = parser.get_question_type()
        if choice_strategy == "correct":
            self._choice = parser.correct()
        elif choice_strategy == "incorrect":
            self._choice = parser.incorrect()
        elif choice_strategy == "random":
            self._choice = parser.random()
        else:
            raise ValueError(f"Unknown choice strategy: {choice_strategy}")

        return self

    def build(self) -> Answer:
        # Must have type, choice, question_index from either manual or parser
        if self._type is None or self._choice is None or self._question_index is None:
            raise ValueError("AnswerBuilder is missing required fields")

        content = Content(
            type=self._type,
            choice=self._choice,
            questionIndex=self._client_info.get_question_index()
        )

        data = DataPayload(
            gameid=self._client_info.get_gameid(),
            type="message",
            host="kahoot.it",
            id=self._client_info.get_id(),
            content=orjson.dumps(content.model_dump()).decode("utf-8")
        )

        return Answer(
            id=str(self._client_info.get_id()),
            channel="/service/controller",
            data=data,
            clientId=self._client_info.get_clientid(),
            ext={}
        )


# To properly answer a question in Kahoot, you must follow a specific control flow:
#
# 1. Receive the answer metadata:
#    - This is a message containing basic information about the upcoming question.
#    - It usually has an "id" of 1.
#
# 2. Send a heartbeat message:
#    - Immediately after receiving the metadata, send a generic heartbeat message.
#    - This signals to the Kahoot server that you're ready.
#
# 3. Receive the full game block:
#    - After the heartbeat, the server will send the actual message.
#    - This contains the full details of the question (e.g., type, choices, etc.).
#
# Only after receiving the gameBlock should you attempt to build and send your answer.



    
    


