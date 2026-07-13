"""
reconnect_manager.py
Recon Rover V1 - Serial Communication Manager

Handles exponential backoff logic for reconnecting.
"""

import asyncio

class ReconnectManager:
    def __init__(self, initial_delay: float = 1.0, max_delay: float = 10.0, backoff_factor: float = 1.5):
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self._current_delay = initial_delay

    async def wait_before_reconnect(self):
        """
        Sleeps for the current backoff delay, then increases it.
        """
        await asyncio.sleep(self._current_delay)
        
        self._current_delay *= self.backoff_factor
        if self._current_delay > self.max_delay:
            self._current_delay = self.max_delay

    def reset_backoff(self):
        """
        Resets the delay after a successful connection is established.
        """
        self._current_delay = self.initial_delay
