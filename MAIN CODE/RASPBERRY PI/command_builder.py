"""
command_builder.py
Recon Rover V1 - Command Builder

Core engine orchestrating semantic events into protocol CommandPackets.
"""

from lifecycle_manager import BaseModule
from event_bus import (
    EventBus, MovementRequestEvent, EmergencyStopRequested, 
    HazardDetected, BatteryCritical, RecoveryStarted
)

from command_builder.command_factory import CommandFactory
from command_builder.command_validator import CommandValidator
from command_builder.command_queue import CommandQueue
from command_builder.command_scheduler import CommandScheduler
from command_builder.command_health import CommandHealthMonitor

class CommandBuilder(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.factory = CommandFactory()
        self.validator = CommandValidator()
        self.queue = CommandQueue(max_size=50)
        self.scheduler = CommandScheduler(self.queue, self.event_bus, rate_limit_ms=20)
        self.health_monitor = CommandHealthMonitor()

    async def initialize(self):
        # Subscribe to semantic intents
        self.event_bus.subscribe(MovementRequestEvent, self._on_movement_request)
        self.event_bus.subscribe(EmergencyStopRequested, self._on_emergency_stop)
        self.event_bus.subscribe(HazardDetected, self._on_hazard)
        self.event_bus.subscribe(BatteryCritical, self._on_battery_critical)
        self.event_bus.subscribe(RecoveryStarted, self._on_recovery)
        
        self.log.info("CommandBuilder initialized.")

    async def start(self):
        self.scheduler.start()
        self.log.info("CommandBuilder started.")

    async def stop(self):
        self.scheduler.stop()
        self.log.info("CommandBuilder stopped.")

    def health(self) -> str:
        depth = self.queue.qsize()
        self.health_monitor.update_queue_depth(depth)
        
        if depth > 40:
            return "DEGRADED_QUEUE_FULL"
        return "OK"

    async def _process_packet(self, packet):
        if not self.validator.validate(packet):
            self.health_monitor.record_validation_failure()
            self.log.warning(f"Validation failed for packet: {packet}")
            return
            
        success = self.queue.put_nowait(packet)
        if not success:
            self.health_monitor.record_drop()
            
        self.health_monitor.update_queue_depth(self.queue.qsize())

    async def _on_movement_request(self, event: MovementRequestEvent):
        packet = self.factory.from_movement_request(event)
        await self._process_packet(packet)

    async def _on_emergency_stop(self, event: EmergencyStopRequested):
        self.health_monitor.record_emergency_stop()
        packet = self.factory.from_emergency_stop(event)
        await self._process_packet(packet)

    async def _on_hazard(self, event: HazardDetected):
        packet = self.factory.from_hazard(event)
        await self._process_packet(packet)

    async def _on_battery_critical(self, event: BatteryCritical):
        packet = self.factory.from_battery_critical(event)
        await self._process_packet(packet)

    async def _on_recovery(self, event: RecoveryStarted):
        packet = self.factory.from_recovery(event)
        await self._process_packet(packet)
