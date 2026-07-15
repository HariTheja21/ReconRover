"""
Input Health Module
Recon Rover V2 - Phase 2.6

Publishes health snapshots of the controller/input subsystem to the EventBus.
"""

from typing import Any
from dataclasses import dataclass
from .input_statistics import InputStatistics

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class InputHealthUpdated(Event):
    is_connected: bool
    device_name: str
    raw_events_rx: int
    events_dropped_deadzone: int
    intents_generated: int

class InputHealth:
    """Periodically retrieves stats and publishes."""
    
    def __init__(self, event_bus: Any, stats: InputStatistics):
        self._bus = event_bus
        self._stats = stats
        self.is_connected = False
        self.device_name = "None"
        
    def broadcast(self):
        """Dispatches the current input metrics."""
        snapshot = self._stats.get_snapshot()
        
        event = InputHealthUpdated(
            is_connected=self.is_connected,
            device_name=self.device_name,
            raw_events_rx=snapshot["raw_events_rx"],
            events_dropped_deadzone=snapshot["events_dropped_deadzone"],
            intents_generated=snapshot["intents_generated"]
        )
        self._bus.publish(event)
