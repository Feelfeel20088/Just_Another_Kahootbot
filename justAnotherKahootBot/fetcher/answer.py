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


class KahootMessage(BaseModel):
    id: str
    channel: str
    data: DataPayload
    clientId: str
    ext: Dict[str, Any]



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

class ClientInfo:
    __nickname: str
    __gameid: str
    __clientid: str
    __question_index: int = -1
    __ack: int = 2
    __id: int = 6
    

    # getter / setters

    def get_nickname(self) -> str:
        return self.__nickname

    def set_nickname(self, value) -> str:
        self.__nickname = value

    def set_gameid(self, value: str):
        self.__gameid = value

    def get_gameid(self) -> str:
        return self.__gameid

    
    def set_gameid(self, value: str):
        self.__gameid = value

    
    def get_clientid(self) -> str:
        return self.__clientid

    
    def set_clientid(self, value: str):
        self.__clientid = value

    def get_question_index(self) -> int:
        self.__question_index =+ 1
        return self.__question_index


    def get_ack(self) -> int:
        self.__ack =+ 1
        return self.__ack


    def get_id(self) -> int:
        self.__id =+ 1
        return self.__id


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

    def build(self) -> KahootMessage:
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

        return KahootMessage(
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

class Answer:

    @classmethod
    async def send_answer(ws, context: ClientInfo, answer_data: KahootMessage):
        """Send a built Kahoot answer through the websocket."""
        t = time.time()
        
        await ws.send(orjson.dumps(answer_data.model_dump()).decode())

        elapsed = time.time() - t
        
        logger.debug(
            f"Bot '{context.get_nickname()}' sent answer in {elapsed:.4f}s | "
            f"Choice: {answer_data.data.content.choice} | Type: {answer_data.data.content.type}"
        )
    @classmethod
    async def generic_heartbeat(ws, context: ClientInfo, answer_data: KahootMessage):

        await self.ws.send(self.payloads.__heartBeat__(self.clientInfo.get_id(), self.clientInfo.get_act()))


    
    


