import asyncio
import uuid
from time import time
from typing import List
import traceback
from .kahootBot import KahootBot
import secrets
from justAnotherKahootBot.config.logger import logger
from .exceptions import FatalError, SwarmHandler, TaskCrash
from justAnotherKahootBot.api.context import Context


class Swarm:
    def __init__(self):
        """Initialize the swarm object."""
        self.id = uuid.uuid4()
        self.context: Context = Context()
        # self.context.addSwarm(self.id, self)
        self.ttl = None
        self.start_time = time()
        self.tasks: List[asyncio.Task] = []
        self.gameid: int
        self.nickname: str
        self.crash: bool
        self.queue = asyncio.Queue(maxsize=100)  # Errors will be put in here
        self.instancetotask: dict[KahootBot, asyncio.Task] = {}
        self.stop = False
        self.clean_execution: FatalError = None

    def getSwarmId(self):
        """Gets the Swarms uuid"""
        return self.id

    def isAlive(self) -> bool:
        """Check if the swarm is still alive based on TTL."""
        return (time() - self.start_time) < self.ttl

    def getTimeRemaining(self) -> int:
        """Calculate the time remaining before TTL expires."""
        return self.ttl - (time() - self.start_time)

    def startNewBot(self):
        """Start a new bot instance and create its task."""
        # if the instance is one simply name the bot without the hash
        if self.amount == 1: 
            instance = KahootBot(self.gameid, self.nickname, self.crash, self.queue)
        else: 
            instance = KahootBot(self.gameid, f"{self.nickname}{secrets.token_hex(4)}", self.crash, self.queue)
        
        task = instance.startBot()
        self.instancetotask[instance] = task
        self.tasks.append(task)


    def killSwarm(self, error: SwarmHandler):
        """ends the swarm"""
        self.clean_execution = error
        self.stop = True


    async def stopBot(self, instance: KahootBot, task: asyncio.Task):
        """stops a bot"""

        task.cancel()

        await task
        logger.debug(f"Bot {instance.nickname} has been removed on the swarm side.")
        self.tasks.remove(task)

        del self.instancetotask[instance]

    async def cleanUp(self, timeout: float = 5.0):
        """Cancel all running tasks with timeout and diagnostics."""
        try:
            for index, task in enumerate(self.tasks):
                if task.done():
                    logger.debug(f"Swarm {self.id}'s bot {index} already completed.")
                    
                    e = task.exception()
                    if e:
                        logger.debug(f"Cleanup found error in kahoot bot {index} in swarm {self.id}. Error: {e}")
                        self.clean_execution = TaskCrash(e)
                    continue

                task.cancel()
                try:
                    await asyncio.wait_for(task, timeout=timeout)
                    logger.debug(f"Swarm {self.id}'s bot {index} closed cleanly.")
                except asyncio.TimeoutError:
                    logger.warning(
                        f"Swarm {self.id}'s Bot {index} did NOT shut down in {timeout}s. "
                        "The bot is not being tracked anymore and may be a zombie task."
                    )
                    self.clean_execution = TaskCrash("task timeout while waiting for it to be cancled")

                except Exception as e:
                    logger.exception(f"Swarm {self.id}'s Bot {index} crashed during cleanup: {e}")

            self.watchdog.cancel()    
            await self.watchdog 
            self.tasks.clear()
            self.instancetotask.clear()
            # self.context.removeSwarm(self.id)
            
        except Exception as e:
            logger.exception(f"swarm {self.id} Failed during cleanup")



    
    # watch dog is for kahoot events that need to 
    # trigger a certin action in swarm, NOT for monitoring tasks. 
    # We dont monitor tasks. Rather we will wait till the swarms 
    # timeout to check if tasks died or not. 
    async def watchDog(self):
    
        while True:

            try:
                instance, error = await self.queue.get()
                await error.handle(instance, self.instancetotask[instance], self)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"default exception caught in swarm {self.id}:", e)

    async def start(self, gameid: int, nickname: str, crash: bool, amount: int, ttl: int):
        """Start the swarm in an async event loop with TTL check."""
        try:
            self.gameid = gameid
            self.nickname = nickname
            self.crash = crash
            self.amount = amount
            logger.debug(f"starting {amount} kahoot bot(s) in swarm {self.id} ...")

            self.watchdog = asyncio.create_task(self.watchDog())

            
            for _ in range(int(amount)):
                self.startNewBot()

            # set ttl after bots have started to 
            # make sure bots init dont take up lifetime
            self.ttl = int(ttl)
            logger.debug("Time Starting...")
            # Main loop to check if the swarm is still alive
            while self.isAlive() and not self.stop:
                logger.info("time remaining: " + str(self.getTimeRemaining()) + "Amount of bots: " + str(len(self.tasks)))
                await asyncio.sleep(10)

            await self.cleanUp()

            if not self.clean_execution:
                e = "successfully"
            else:
                e = f"with a error: {type(self.clean_execution).__name__} error details: {self.clean_execution}"
            logger.info(f"Swarm {self.id} with {amount} bot(s) and a lifetime of {ttl} second(s) closed {e}")
        except Exception as e:
            logger.error(f"Found error in swarm {self.id}: {e}")


    # Task starter for the /swarm endpoint wrapped in a new task as we dont want the endpoint to live for the entire duration of the swarm.
    def createSwarm(self, gameid: int, nickname: str, crash: bool, amount: int, ttl: int):
        """Create a new swarm task and run it asynchronously."""
        logger.info(f"New swarm creation started. Amount: {amount}, TTL: {ttl}, nickname: {nickname}")
        asyncio.create_task(self.start(gameid, nickname, crash, amount, ttl))
