"""
reconnect_manager.py
Recon Rover V1 - Hardware Interface

Manages automatic connection recovery via exponential backoff.
"""

import asyncio
from .connection_manager import ConnectionManager

class ReconnectManager:
    def __init__(self, conn_manager: ConnectionManager):
        self.conn_manager = conn_manager
        self.reconnect_task = None
        
    def trigger_reconnect(self):
        """Starts the reconnect loop if not already running."""
        if self.reconnect_task is None or self.reconnect_task.done():
            self.reconnect_task = asyncio.create_task(self._reconnect_loop())
            
    def stop(self):
        if self.reconnect_task:
            self.reconnect_task.cancel()
            
    async def _reconnect_loop(self):
        attempt = 1
        while not self.conn_manager.connected:
            success = await self.conn_manager.attempt_connect()
            if success:
                break
                
            # Exponential backoff (max 10 seconds)
            wait_time = min(10.0, 2 ** attempt)
            await asyncio.sleep(wait_time)
            attempt += 1
