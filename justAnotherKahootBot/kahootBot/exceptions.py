
import asyncio
from ...config.logger import logger
class SwarmHandler(Exception):
    async def handle(self, instance, task: asyncio.Task, swarm):
        raise NotImplementedError(f"handle is not implemented for {self.__class__.__name__}!")
    



class KickedFromGameError(SwarmHandler):
    """Thrown when the host of the kahoot game kicks out the bot"""

    async def handle(self, instance, task: asyncio.Task, swarm):
        
        # simply restart the bot
        await swarm.stopBot(instance, task)
        swarm.startNewBot()

class TooManyPlayersError(SwarmHandler):
    async def handle(self, instance, task: asyncio.Task, swarm):
        await swarm.stopBot(instance, task)


class FatalError(SwarmHandler):
    async def handle(self, instance, task: asyncio.Task, swarm):
        # simply restart the bot 
        swarm.killSwarm(self)


class HostDisconnectError(FatalError):
    pass

class SessionNotFoundError(FatalError):
    pass
class GameEndedError(FatalError):
    pass

class UnknownJsonModelException(FatalError):
    pass
        