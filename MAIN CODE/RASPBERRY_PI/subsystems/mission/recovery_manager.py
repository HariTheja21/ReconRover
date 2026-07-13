"""
recovery_manager.py
Recon Rover V1 - Behavior Engine

Handles automated recovery from deadlocks, obstacles, and system failures.
"""

from logger import Logger
from event_bus import EventBus
import time
from dataclasses import dataclass

@dataclass
class RecoveryEvent:
    pass

class RecoveryTriggered(RecoveryEvent):
    reason: str

class RecoveryManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.log = Logger.get("RecoveryManager")
        self._stuck_time_ms = 0
        self._last_tick_ms = int(time.time() * 1000)

    def tick(self, is_stuck: bool):
        now = int(time.time() * 1000)
        dt = now - self._last_tick_ms
        self._last_tick_ms = now

        if is_stuck:
            self._stuck_time_ms += dt
            if self._stuck_time_ms > 5000: # 5 seconds stuck
                self.log.warning("Deadlock detected. Triggering recovery protocol.")
                # Self-healing logic would go here, e.g. emitting a reverse command
                self._stuck_time_ms = 0 # reset after trigger
        else:
            self._stuck_time_ms = max(0, self._stuck_time_ms - dt)
