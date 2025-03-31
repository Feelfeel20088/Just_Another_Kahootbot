import requests
import asyncio
import websockets
import random
import uuid
import time
from .payloads import Payloads
from .exceptions import *
from ..challenge.runchallenge import runChallenge
from .exceptions import SwarmHandler
from ..logger import logger
from ..events import compare_models_to_ingress_json
import orjson







class KahootBot:

    def __init__(self, gameid: int, nickname: str, crash: bool, queue: asyncio.Queue):
        self.gameid = gameid
        self.nickname = nickname
        self.crash = crash
        self.ack = 2
        self.id = 6
        self.wsocket = None
        self.errorHandler = queue
        self.sendHartebeat = True
        self.childTasks = []

    def start(self):
        return asyncio.create_task(self.watchDog())

    async def watchDog(self):
        try: 
            await self.connect()
            while True:
                for task in self.childTasks:
                    if task.done():
                        if isinstance(task.exception(), SwarmHandler):
                            await self.errorHandler.put((self, task.exception()))
                            logger.error(f"watchDog: {task.exception()} type: {type(task.exception())}")
                            return
                        logger.error(f"watchDog found an unhandled error: {task.exception()}")
                        return
                await asyncio.sleep(5)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"WatchDog found a unhandled error in connect(): {e}")
        finally:
            await self.cleanUp()

    async def connect(self):
        """Handles connecting to the Kahoot WebSocket server."""
        cookies = {
            "generated_uuid": str(uuid.uuid4()),
            "player": "active"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }

        response = requests.get(
            f'https://kahoot.it/reserve/session/{self.gameid}/?{time.time()}',
            headers=headers,
            cookies=cookies
        )
        response.raise_for_status()
        
        

       
        challenge_response = runChallenge(response.json()['challenge'], response.headers['x-kahoot-session-token'])
        

        logger.info(f"WebSocket URL: wss://kahoot.it/cometd/{self.gameid}/{challenge_response}")

        logger.info(f"Connecting to WebSocket...")
    
        self.wsocket = await websockets.connect(
            f'wss://kahoot.it/cometd/{self.gameid}/{challenge_response}',
            ping_interval=30, 
            ping_timeout=60,
            open_timeout=30
        )
        logger.info(f"Connected!")
        await self.initialize_connection()
        self.childTasks.append(asyncio.create_task(self.heartBeat()))
        self.childTasks.append(asyncio.create_task(self.receiveMessages()))
            
        if self.crash:
            self.childTasks.append(asyncio.create_task(self.crasher()))

    async def initialize_connection(self):
        """Handles initial WebSocket handshakes."""
        await self.wsocket.send(Payloads.__connect__())
        response = orjson.loads(await self.wsocket.recv())
        client_id = response[0]["clientId"]
        self.payloads = Payloads(self.gameid, client_id)

        # Send authentication messages
        await self.wsocket.send(self.payloads.__clientId__())
        await self.wsocket.send(self.payloads.__clientId2__())
        await self.wsocket.send(self.payloads.__connectID__(self.nickname))
        await self.wsocket.send(self.payloads.__keepInGame__())
        await self.wsocket.send(self.payloads.__metaConnect__())

    async def receiveMessages(self):
        """Receives and logs messages from the WebSocket."""
        try:
            async for message in self.wsocket:
                logger.debug(f"Received raw message: {message}")
                 
                await compare_models_to_ingress_json(message, self)
                
                
    
        except asyncio.CancelledError:
            return

    async def heartBeat(self):
        """Sends periodic heartbeat messages to keep the connection alive."""
        try:
            while True:
                if self.sendHartebeat:
                    self.id += 1
                    self.ack += 1
                    logger.debug(f"ID is at {self.id}")
                    logger.debug(f"Sending heartbeat: {self.payloads.__heartBeat__(self.id, self.ack)}")
                    await self.wsocket.send(self.payloads.__heartBeat__(self.id, self.ack))
                await asyncio.sleep(3)
        except asyncio.CancelledError:
            return
        
    async def standAloneHeartBeat(self):
        self.id += 1
        self.ack += 1
        await self.wsocket.send(self.payloads.__heartBeat__(self.id, self.ack))
        logger.debug(f"Sent standalone heartbeat")

    async def answerQuestion(self, choice, type):
        """Handles answering Kahoot questions."""
    
        self.id += 1
        logger.debug(f"Sending answer choice: {choice}")
        await self.wsocket.send(self.payloads.__answerQuestion__(self.id, choice, type))
        logger.info(f"Answer sent. choice: {choice}")

    async def crasher(self): 
        try:
            while True:
                logger.debug(self.payloads.__crash__(self.id))
                await self.wsocket.send(self.payloads.__crash__(self.id)) 
                await asyncio.sleep(1)
                logger.debug("here")
        except asyncio.CancelledError:
            return

    async def cleanUp(self):
        for task in self.childTasks:
            if not task.done():  # Only cancel tasks that are still running
                task.cancel()
                try:
                    await task  # Ensure graceful cancellation
                except Exception as e:
                    logger.error(f"Error during cleanup: {e}")  # Handle other unexpected errors

        self.childTasks.clear()

        if self.wsocket:
            await self.wsocket.close()

        logger.info(f"Cleanup completed, tasks canceled, WebSocket closed.")
