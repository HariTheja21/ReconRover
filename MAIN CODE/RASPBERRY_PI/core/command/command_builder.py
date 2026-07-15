"""
Command Builder Module
Recon Rover V2 - Phase 2.5

The central orchestrator for outbound logic.
Subscribes to cognitive intents, validates them against the current system state,
encodes them to binary, and routes them to the physical queue.
"""

import sys
import os
import asyncio
from typing import Any

from .command_events import (
    MoveIntent, StopIntent, ServoIntent, ModeChangeIntent, MissionChangeIntent, EmergencyStopIntent,
    CommandValidated, CommandRejected, CommandQueued, OutgoingCommandPacket
)
from .command_validator import CommandValidator
from .command_encoder import CommandEncoder
from .command_queue import CommandQueue
from .command_statistics import CommandStatistics
from .command_health import CommandHealth
from .command_scheduler import CommandScheduler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from enums import PacketPriority
except ImportError:
    class PacketPriority: CRITICAL = 3; HIGH = 2; NORMAL = 1; LOW = 0

class DummyState:
    """Fallback state cache if Phase 2.2 state manager isn't linked."""
    def __init__(self):
        self.safety_state = 0
        self.operating_mode = 2 # SMART_CONTROL
        self.is_locked = False
        self.lock_reason = ""
        self.sensors_healthy = True

class CommandBuilder:
    """
    Traffic controller for outbound intent.
    """
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = CommandStatistics()
        
        self.queue = CommandQueue(max_size=100)
        self.scheduler = CommandScheduler(self._bus, self.queue, self.stats)
        self.health = CommandHealth(self._bus, self.stats, lambda: self.queue.qsize)
        
        # In a real integration, this is updated by Phase 2.2 StateManager
        self.current_state = DummyState()
        
        self._subscribe_intents()
        
    def _subscribe_intents(self):
        """Bind to all outbound intent events."""
        self._bus.subscribe(MoveIntent, self._handle_move)
        self._bus.subscribe(StopIntent, self._handle_stop)
        self._bus.subscribe(ServoIntent, self._handle_servo)
        self._bus.subscribe(ModeChangeIntent, self._handle_mode)
        self._bus.subscribe(MissionChangeIntent, self._handle_mission)
        self._bus.subscribe(EmergencyStopIntent, self._handle_estop)
        
    def start(self):
        """Starts the scheduler."""
        self.scheduler.start()
        
    def stop(self):
        """Stops the scheduler."""
        self.scheduler.stop()
        
    def _process_intent(self, intent: Any, target_priority: int):
        """Core logic to validate, encode, and enqueue an intent."""
        self.stats.add_processed()
        intent_name = type(intent).__name__
        
        # 1. Validate
        is_valid, reason = CommandValidator.validate(intent, self.current_state)
        if not is_valid:
            self.stats.add_rejected()
            self._bus.publish(CommandRejected(intent_type=intent_name, reason=reason))
            return
            
        self._bus.publish(CommandValidated(intent_type=intent_name))
        
        # 2. Encode
        packet: OutgoingCommandPacket = CommandEncoder.encode(intent, target_priority)
        
        # 3. Enqueue
        if self.queue.enqueue(packet):
            self._bus.publish(CommandQueued(
                priority=target_priority, 
                queue_size=self.queue.qsize
            ))
        else:
            self.stats.add_rejected()
            self._bus.publish(CommandRejected(intent_type=intent_name, reason="Command Queue Full"))

    # Intent Handlers map priorities
    async def _handle_move(self, intent: MoveIntent):
        self._process_intent(intent, getattr(PacketPriority, 'HIGH', 2))
        
    async def _handle_stop(self, intent: StopIntent):
        self._process_intent(intent, getattr(PacketPriority, 'CRITICAL', 3))
        
    async def _handle_estop(self, intent: EmergencyStopIntent):
        self._process_intent(intent, getattr(PacketPriority, 'CRITICAL', 3))
        
    async def _handle_servo(self, intent: ServoIntent):
        self._process_intent(intent, getattr(PacketPriority, 'NORMAL', 1))
        
    async def _handle_mode(self, intent: ModeChangeIntent):
        self._process_intent(intent, getattr(PacketPriority, 'NORMAL', 1))
        
    async def _handle_mission(self, intent: MissionChangeIntent):
        self._process_intent(intent, getattr(PacketPriority, 'NORMAL', 1))
