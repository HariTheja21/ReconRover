"""
telemetry_manager.py
Recon Rover V1 - Cognitive Layer

Maintains the global state of the robot based on incoming telemetry.
"""

from lifecycle_manager import BaseModule
from event_bus import EventBus, TelemetryReceived

class TelemetryManager(BaseModule):
    """
    Subscribes to telemetry events and provides access to the latest state.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self._latest_state = {}
        
    async def initialize(self):
        self.event_bus.subscribe(TelemetryReceived, self._on_telemetry)
        self.log.info("TelemetryManager initialized.")

    async def start(self):
        self.log.info("TelemetryManager started.")

    async def stop(self):
        self.log.info("TelemetryManager stopped.")

    async def _on_telemetry(self, event: TelemetryReceived):
        """Update internal state when new telemetry arrives."""
        self._latest_state = event.data
        # In the future, this module might publish specific abstracted events,
        # like ObstacleDetected or BatteryLow, based on raw telemetry parsing.

    def get_latest_state(self) -> dict:
        return self._latest_state
