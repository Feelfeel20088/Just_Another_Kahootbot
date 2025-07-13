from pydantic import BaseModel
from typing import Optional, Dict, Any
from .clientInfo import ClientInfo
import orjson
from justAnotherKahootBot.config.logger import logger

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




class AnswerBuilder:
    def __init__(self, client_info: ClientInfo):
        self._client_info = client_info
        self._type: Optional[str] = None
        self._choice: Optional[int] = None
        self._question_index: Optional[int] = None

    def set_type(self, question_type: str):
        self._type = question_type
        return self

    def set_choice(self, choice: int):
        self._choice = choice
        return self

    def set_random_choice(self, max_choice: int):
        self._choice = random.randint(0, max_choice - 1)
        return self

    def set_question_index(self, index: int):
        self._question_index = index
        return self

    def build(self) -> KahootMessage:
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

        t = t - time.time()

        elapsed = time.time() - start_time
        
        logger.debug(
            f"Bot '{context.get_nickname()}' sent answer in {elapsed:.4f}s | "
            f"Choice: {answer_data.data.content.choice} | Type: {answer_data.data.content.type}"
        )
    @classmethod
    async def generic_heartbeat(ws, context: ClientInfo, answer_data: KahootMessage):

        await self.ws.send(self.payloads.__heartBeat__(self.clientInfo.get_id(), self.clientInfo.get_act()))


    
    


