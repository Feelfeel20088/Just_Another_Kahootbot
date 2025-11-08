import httpx
import asyncio
import websockets
import random
import uuid
import time
from .payloads import Payloads
from .clientInfo import ClientInfo
from .answer import Answer
from .exceptions import *
from justAnotherKahootBot.challenge.runchallenge import Challenge 
from .exceptions import SwarmHandler
from justAnotherKahootBot.config.logger import logger
from justAnotherKahootBot.events import compare_models_to_ingress_json
import orjson







class KahootBot:

    def __init__(self, gameid: int, nickname: str, crash: bool, queue: asyncio.Queue):
        self.clientInfo = ClientInfo()
        self.clientInfo.set_gameid(gameid)
        self.clientInfo.set_nickname(nickname)
        self.crash = crash
        self.wsocket = None
        self.errorHandler = queue
        self.childTasks = []
        self.timeout = 10.0 

    def get_nickname(self):
        return self.clientInfo.get_nickname();

    def startBot(self) -> None:
        """Starts a bot in a task"""
        return asyncio.create_task(self.connect())

    # async def watchDog(self):
    #     try: 
    #         await self.connect()
    #         while True:
    #             for task in self.childTasks:
    #                 if task.done():
                        
    #                     if isinstance(task.exception(), SwarmHandler):
    #                         await self.errorHandler.put((self, task.exception()))
    #                         logger.warning(f"watchDog: {task.exception()} type: {type(task.exception())}")
    #                         return
    #                     logger.error(f"watchDog found an unhandled error: {task.exception()}")
    #                     return
    #             await asyncio.sleep(3)

    #     except asyncio.CancelledError:
    #         pass
    #     except Exception as e:
    #         logger.error(f"WatchDog found a unhandled error in connect(): {e}")
    #     finally:
    #         await self.cleanUp()


    async def connect(self):
        """Handles connecting to the Kahoot WebSocket server."""

        
        
        cookies = {
            "generated_uuid": str(uuid.uuid4()),
            "player": "active"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'https://kahoot.it/reserve/session/{self.clientInfo.get_gameid()}/?{time.time()}',
                    headers=headers,
                    cookies=cookies,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                try:
                    json_data = orjson.loads(response.content)
                except orjson.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    raise
                session_token = response.headers.get('x-kahoot-session-token')
                if not session_token:
                    logger.error("Missing 'x-kahoot-session-token' header in response")
                    raise

                challenge_response = Challenge.run_challenge(json_data['challenge'], session_token)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.reason_phrase}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

        logger.info(f"WebSocket URL: wss://kahoot.it/cometd/{self.clientInfo.get_gameid()}/{challenge_response}")
        logger.info("Connecting to WebSocket...")

        self.wsocket = await websockets.connect(
            f'wss://kahoot.it/cometd/{self.clientInfo.get_gameid()}/{challenge_response}',
            ping_interval=30,
            ping_timeout=60,
            open_timeout=30
        )
        self.wsocket

        logger.info("Connected!")

        await self.initialize_connection()
        self.childTasks.append(asyncio.create_task(self.heartBeat()))
        self.childTasks.append(asyncio.create_task(self.receiveMessages()))

        if self.crash:
            self.childTasks.append(asyncio.create_task(self.crasher()))

        try:
            while True:
                await asyncio.sleep(3)

        except asyncio.CancelledError:
            await self.cleanUp()
            logger.debug("Bot has been cleaned up bot side")
        

    async def initialize_connection(self) -> None:
        """Handles initial WebSocket handshakes."""
        await self.wsocket.send(Payloads.__connect__())
        response = orjson.loads(await self.wsocket.recv())
        client_id = response[0]["clientId"]

        self.clientInfo.set_clientid(client_id)

        self.payloads = Payloads(self.clientInfo.get_gameid(), client_id)

        # Send authentication messages
        await self.wsocket.send(self.payloads.__clientId__())
        await self.wsocket.send(self.payloads.__clientId2__())
        await self.wsocket.send(self.payloads.__connectID__(self.clientInfo.get_nickname()))
        await self.wsocket.send(self.payloads.__keepInGame__())
        await self.wsocket.send(self.payloads.__metaConnect__())

    async def receiveMessages(self) -> None:
        """Receives and logs messages from the WebSocket."""
        try: 
            async for message in self.wsocket:
                try:
                    await compare_models_to_ingress_json(message, self)
                except FatalError as e:
                    logger.debug(f"Caught Swarm Fatel exception: {e}")
                    await self.errorHandler.put((self, e))
                except SwarmHandler as e:
                    await self.errorHandler.put((self, e))
                except Exception as e:
                    logger.exception("found exception in model hander")
                    
                

        
        except asyncio.CancelledError:
            return

    
        

    async def heartBeat(self) -> None:
        """Sends periodic heartbeat messages to keep the connection alive."""
        try:
            while True:
                await self.wsocket.send(self.payloads.__heartBeat__(self.clientInfo.get_id(), self.clientInfo.get_ack()))
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            return
        
    async def standAloneHeartBeat(self) -> None:
        self.id += 1
        self.ack += 1
        await self.wsocket.send(self.payloads.__heartBeat__(self.clientInfo.get_id(), self.clientInfo.get_ack()))

    async def crasher(self) -> None: 
        try:
            while True:
                logger.debug("debug crash")
                await self.wsocket.send(self.payloads.__crash__(self.clientInfo.get_id())) 
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            return

    async def cleanUp(self) -> None:
        for task in self.childTasks:
            if not task.done():  # Only cancel tasks that are still running
                task.cancel()
                try:
                    logger.debug(f"Cleaning up tasks in bot {self.clientInfo.get_nickname()}")
                    await task  # Ensure graceful cancellation 
                except Exception as e:
                    logger.error(f"Error during cleanup: {e}")  # Handle other unexpected errors

        self.childTasks.clear()

        if self.wsocket:
            await self.wsocket.close()

        logger.debug(f"Cleanup completed, tasks canceled, WebSocket closed.")
