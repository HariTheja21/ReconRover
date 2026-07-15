import asyncio
from .boot_engine import BootEngine

class BootManager:
    def __init__(self, publish_callback):
        self.publish = publish_callback
        self.engine = BootEngine(publish_callback)

    async def start_system(self) -> bool:
        """
        Entry point to start the entire robot software stack.
        """
        return await self.engine.execute_boot()
