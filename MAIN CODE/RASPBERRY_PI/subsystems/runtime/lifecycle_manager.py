"""
lifecycle_manager.py
Recon Rover V1 - Full System Integration

Defines the absolute base contract for all system modules.
(In a real deployment, existing modules inherit from this or wrap this).
"""

import logging

class BaseModule:
    """The abstract contract every subsystem must implement to join the Runtime."""
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self._health_status = "UNKNOWN"
        
    async def initialize(self):
        """Called once during the startup phase. Used for allocating resources."""
        pass
        
    async def start(self):
        """Called once to begin processing (e.g., spawn asyncio tasks)."""
        pass
        
    async def stop(self):
        """Called during shutdown. Must safely release resources."""
        pass
        
    def health(self) -> str:
        """Returns the internal health state: OK, DEGRADED, FATAL."""
        return self._health_status
