class Context:
    _instance = None
    def __init__(self):
        self._swarm_info = {}


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def addSwarm(self, id, swarm):
        self._swarm_info[id] = swarm

    def removeSwarm(self, id):
        del self._swarm_info[id]

    def getSwarm(self, id):
        return self._swarm_info[id]

    def getSwarmList(self):
        return dict(self._swarm_info)  