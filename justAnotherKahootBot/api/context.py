import asyncio
import gc
import sys
import logging

logger = logging.getLogger(__name__)
class Context:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._swarm_info = {}
        return cls._instance

    def addSwarm(self, id, swarm):
        self._swarm_info[id] = swarm

    def removeSwarm(self, id):
        if id in self._swarm_info:
            del self._swarm_info[id]

    def getSwarm(self, id):
        return self._swarm_info.get(id)

    def getSwarmList(self):
        return dict(self._swarm_info)

    async def watchdog(self):
            """Periodically cleans up inactive swarm instances."""
            while True:
                await asyncio.sleep(5)
                for swarm_id in list(self._swarm_info.keys()):
                    swarm = self._swarm_info[swarm_id]
                    if getattr(swarm, "done", False):
                        logger.info(f"[Watchdog] Swarm {swarm_id} marked done — inspecting references...")

                        # print reference count
                        logger.debug(f"Refcount: {sys.getrefcount(swarm) - 1}")

                        # show what objects reference it
                        refs = gc.get_referrers(swarm)
                        logger.debug(f"Found {len(refs)} referrers:")
                        for r in refs:
                            logger.debug(f" - {type(r)} {getattr(r, '__name__', '')}")

                        # now try to delete
                        del self._swarm_info[swarm_id]
                        logger.info(f"[Watchdog] Removed swarm {swarm_id} from _swarm_info.")

                gc.collect()