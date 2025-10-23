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