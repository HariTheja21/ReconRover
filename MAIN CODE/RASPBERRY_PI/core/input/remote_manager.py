"""
Remote Manager Module
Recon Rover V2 - Phase 2.6

The central orchestrator for physical inputs.
Binds OS-level controller callbacks, routes data through mappers and validators,
and publishes semantic intents onto the EventBus.
"""

from typing import Any
import asyncio

from .input_events import RawJoystickMoved, RawButtonPressed
from .input_validator import InputValidator
from .joystick_mapper import JoystickMapper
from .button_mapper import ButtonMapper
from .gamepad_manager import GamepadManager
from .input_statistics import InputStatistics
from .input_health import InputHealth

class RemoteManager:
    """Manages the full lifecycle of physical human input."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        
        self.stats = InputStatistics()
        self.health = InputHealth(self._bus, self.stats)
        
        self.validator = InputValidator()
        self.joy_mapper = JoystickMapper(deadzone=0.15)
        self.btn_mapper = ButtonMapper()
        
        self.gamepad = GamepadManager()
        self.gamepad.on_axis_moved = self._handle_raw_axis
        self.gamepad.on_button_pressed = self._handle_raw_button
        
        self._running = False
        self._poll_task = None
        
    def start(self):
        """Attempts to connect hardware and starts the polling loop."""
        if self.gamepad.connect():
            self.health.is_connected = True
            self.health.device_name = "Generic USB Controller"
        else:
            self.health.is_connected = False
            self.health.device_name = "None"
            
        self.health.broadcast()
        
        self._running = True
        # Even without a controller, we keep the loop alive so test mocks can pump data
        self._poll_task = asyncio.create_task(self._poll_loop())
        
    def stop(self):
        self._running = False
        if self._poll_task:
            self._poll_task.cancel()

    async def _poll_loop(self):
        """Background coroutine to poll hardware."""
        while self._running:
            self.gamepad.poll()
            await asyncio.sleep(0.02) # 50Hz polling rate
            
    def _handle_raw_axis(self, axis_id: int, value: float):
        """Callback from GamepadManager."""
        self.stats.add_rx()
        
        is_valid, clamped_val = self.validator.validate_axis(value)
        if not is_valid:
            # We still proceed with the clamped value to prevent locking up,
            # but in a stricter system we might drop it.
            pass
            
        intent = self.joy_mapper.update_axis(axis_id, clamped_val)
        if intent:
            self.stats.add_intent()
            self._bus.publish(intent)
        else:
            # If mapping returns None, it usually means it fell in the deadzone
            # or no motion change occurred.
            self.stats.add_dropped()

    def _handle_raw_button(self, button_id: int):
        """Callback from GamepadManager."""
        self.stats.add_rx()
        
        if not self.validator.validate_button(button_id):
            return
            
        intent = self.btn_mapper.map_button(button_id)
        if intent:
            self.stats.add_intent()
            self._bus.publish(intent)
