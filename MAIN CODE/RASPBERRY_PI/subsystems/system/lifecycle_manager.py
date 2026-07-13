"""
lifecycle_manager.py
Recon Rover V1 - System Orchestrator

The robust implementation of the Lifecycle Manager, tracking states and transitions.
BaseModule remains here so that aliases can forward it seamlessly.
"""

from typing import Dict, Any
import asyncio
from logger import Logger
from event_bus import EventBus
from .application_state import LifecycleState

class BaseModule:
    """Base class for all system modules to enforce lifecycle hooks."""
    def __init__(self):
        self.name = self.__class__.__name__
        self.log = Logger.get(self.name)
        # By default, modules are not tied to the lifecycle_state machine unless registered,
        # but the module_registry will track their state explicitly.

    async def initialize(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    def health(self) -> str:
        return "OK"

class LifecycleManager:
    """
    Manages the overarching startup/shutdown coordination.
    It doesn't directly run modules anymore; the orchestrator's boot/shutdown sequences do.
    This class tracks overall lifecycle progression.
    """
    def __init__(self, event_bus: EventBus):
        self.log = Logger.get("LifecycleManager")
        self.event_bus = event_bus
        self._shutdown_event = asyncio.Event()

    async def wait_for_shutdown(self):
        """Block until a shutdown completes."""
        await self._shutdown_event.wait()
        
    def trigger_shutdown(self):
        self._shutdown_event.set()

    # NOTE: startup() and shutdown() methods used in the old version 
    # are removed here. Their responsibilities are taken by boot_sequence.py 
    # and shutdown_sequence.py. However, to maintain some backward compatibility
    # if anything else calls it (main.py is rewritten though), we leave it out.
