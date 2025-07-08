import random
import time
import json

# not my work found on a foram
# TODO make pydamic models for these  

class Payloads:
    
    gameid: str
    clientid: str
    questionIndex: int = 0
    L = random.randint(100, 999),
    O =random.randint(-999, -100)
    

    
    def __init__(self, gameid: str | int, clientid: str) -> None:
        self.clientid = clientid
        self.gameid = str(gameid)

    
        
    def __connect__() -> dict:
        return json.dumps([
            {
                "id": "1",
                "version": "1.0",
                "minimumVersion": "1.0",
                "channel": "/meta/handshake",
                "supportedConnectionTypes": [
                    "websocket",
                    "long-polling",
                    "callback-polling"
                ],
                "advice": {
                    "timeout": 60000,
                    "interval": 0
                },
                "ext": {
                    "ack": True,
                    "timesync": {
                        "tc": str(time.time()),
                        "l": 0,
                        "o": 0
                    }
                }
            }
        ])
    
    
    def __clientId__(self) -> dict:
        return json.dumps([
            {
                "id": "2",
                "channel": "/meta/connect",
                "connectionType": "websocket",
                "advice": {
                    "timeout": 0
                },
                "clientId": self.clientid,
                "ext": {
                    "ack": 0,
                    "timesync": {
                        "tc": str(time.time()),
                        "l": self.L,
                        "o": self.O
                    }
                }
            }
        ])
    
    
    def __clientId2__(self) -> dict:
        return json.dumps([
            {
                "id": "3",
                "channel": "/meta/connect",
                "connectionType": "websocket",
                "clientId": self.clientid,
                "ext": {
                    "ack": 1,
                    "timesync": {
                        "tc": str(time.time()),
                        "l": self.L,
                        "o": self.O
                    }
                }
            }
        ])
    

    # def __clientId3__(self) -> dict:
    #     return json.dumps([
    #         {
    #             "id": "4",
    #             "channel": "/meta/connect",
    #             "connectionType": "websocket",
    #             "clientId": self.clientid,
    #             "ext": {
    #                 "ack": 1,
    #                 "timesync": {
    #                     "tc": str(time.time()),
    #                     "l": random.randint(100, 999),
    #                     "o": random.randint(-999, -100)
    #                 }
    #             }
    #         }
    #     ])
    
    
    def __connectID__(self, name) -> dict:
        return json.dumps([
            {   
                "id": "4",
                "channel": "/service/controller",
                "clientId": self.clientid,
                "data": {
                    "content": "{\"device\":{\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0\",\"screen\":{\"width\":920,\"height\":974}}}",
                    "gameid": self.gameid,
                    "host": "kahoot.it",
                    "name": name,
                    "type": "login"
                },
                "ext": {},
            }
        ])
    
   
    def __keepInGame__(self) -> dict:
        return json.dumps([
            {
                "id": "5",
                "channel": "/service/controller",
                "clientId": self.clientid,
                "data": {
                    "content": "{\"usingNamerator\":false}",
                    "gameid": self.gameid,
                    "host": "kahoot.it",
                    "id": 16,
                    "type": "message"
                },
                "ext": {}
            }
        ])
    

    def __metaConnect__(self) -> dict:
        return json.dumps([
            {
                "id": "6",
                "channel": "/meta/connect",
                "connectionType": "websocket",
                "clientId": self.clientid,
                "ext": {
                    "ack": 2,
                    "timesync": {
                        "tc": str(time.time()),
                        "l": self.L,
                        "o": self.O
                    }
                }
            }
        ])
    

    def __heartBeat__(self, id, ack) -> dict:
        return json.dumps([
            {
                "id": str(id),
                "channel": "/meta/connect",
                "connectionType": "websocket",
                "clientId": self.clientid,
                "ext": {
                    "ack": ack,
                    "timesync": {
                        "tc": str(time.time()),
                        "l": self.L,
                        "o": self.O
                    }
                }
            }
        ])
    
    def __answerQuestion__(self, id: int, choice: int, type: str) -> str:
        payload =  json.dumps([  # Wrap the payload in a list!
            {
                "id": str(id),
                "channel": "/service/controller",
                "data": {
                    "gameid":self.gameid,
                    "type": "message",
                    "host": "kahoot.it",
                    "id": 45,  # Ensure this matches the server's expected ID format
                    "content": json.dumps({
                        "type": type,
                        "choice":random.randint(0,3),
                        "questionIndex":self.questionIndex
                    })
                },
                "clientId": self.clientid,
                "ext": {}
            }
        ])
        self.questionIndex += 1
        return payload


    def __crash__(self, id) -> str:
        return json.dumps([  # Wrap the payload in a list!
            {
                "id": str(id),
                "channel": "/service/controller",
                "data": {
                    "gameid":self.gameid,
                    "type": "message",
                    "host": "kahoot.it",
                    "id": id,  # id to confuse it. if payload is not 45 then it gets confused
                    "content": json.dumps({
                        "type": "quiz",
                        "choice":0,
                        "questionIndex":0
                    })
                },
                "clientId": self.clientid,
                "ext": {}
            }
        ])

