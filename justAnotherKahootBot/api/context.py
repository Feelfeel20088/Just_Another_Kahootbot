class Context:
    _instance = None
    def __init__(self):
        self._swarm_info = []

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def add_swarm(self, swarm):
        self._swarm_info.append(swarm)

    def remove_swarm(self, swarm):
        self._swarm_info.remove(swarm)

    def get_swarm_list(self):
        return list(self._swarm_info)  