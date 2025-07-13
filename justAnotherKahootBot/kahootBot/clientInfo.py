class ClientInfo:
    _nickname: str
    _gameid: str
    _clientid: str
    _question_index: int = -1
    _ack: int = 2
    _id: int = 6
    

    # getter / setters

    def get_nickname(self) -> str:
        return self._nickname

    def set_nickname(self, value) -> str:
        self._nickname = value

    def set_gameid(self, value: str):
        self._gameid = value

    def get_gameid(self) -> str:
        return self._gameid

    
    def set_gameid(self, value: str):
        self._gameid = value

    
    def get_clientid(self) -> str:
        return self._clientid

    
    def set_clientid(self, value: str):
        self._clientid = value

    def get_question_index(self) -> int:
        self._question_index =+ 1
        return self._question_index


    def get_ack(self) -> int:
        self._ack =+ 1
        return self._ack


    def get_id(self) -> int:
        self._id =+ 1
        return self._id