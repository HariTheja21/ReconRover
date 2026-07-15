"""
Safety Manager Module
Recon Rover V2 - Phase 2.2

The active service that monitors system stability.
Subscribes to health, telemetry, battery, and emergency events.
Evaluates vitals via SafetyRules and publishes SafetyStateChanged,
EmergencyStopActivated, or SystemLocked.
"""

import sys
import os
import asyncio
from typing import Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from enums import SafetyState
except ImportError:
    class SafetyState:
        SAFE = 0; WARNING = 1; VIOLATION = 2; EMERGENCY_STOP = 3

# Local imports
from .state_manager import StateManager
from .safety_rules import SafetyRules
from .safety_events import (
    SystemHealthUpdated,
    BatteryUpdated,
    TelemetryUpdated,
    EmergencyButtonPressed,
    SafetyStateChanged,
    EmergencyStopActivated,
    SystemLocked
)

class SafetyManager:
    """
    Monitors system safety boundaries and enforces lockdowns.
    """
    
    def __init__(self, event_bus: Any, state_manager: StateManager):
        """
        Initializes the Safety Manager.
        
        Args:
            event_bus: The central EventBus instance.
            state_manager: The central StateManager instance.
        """
        self._bus = event_bus
        self._state = state_manager
        
        # Subscribe to vitals
        self._bus.subscribe(BatteryUpdated, self._handle_battery_update)
        self._bus.subscribe(SystemHealthUpdated, self._handle_health_update)
        self._bus.subscribe(EmergencyButtonPressed, self._handle_emergency_button)
        
    async def _handle_battery_update(self, event: BatteryUpdated) -> None:
        """Evaluates battery voltage changes."""
        target_state, reason = SafetyRules.evaluate_battery(event.voltage)
        await self._apply_safety_state(target_state, reason)

    async def _handle_health_update(self, event: SystemHealthUpdated) -> None:
        """Evaluates subsystem health reports."""
        target_state, reason = SafetyRules.evaluate_health(event.health_state, event.details)
        await self._apply_safety_state(target_state, reason)
        
    async def _handle_emergency_button(self, event: EmergencyButtonPressed) -> None:
        """Directly triggers an emergency stop."""
        await self._apply_safety_state(SafetyState.EMERGENCY_STOP, f"E-Stop Button Pressed by {event.source}")

    async def _apply_safety_state(self, target_state: int, reason: str) -> None:
        """
        Applies a new safety state if it escalates the current state, 
        or if recovery conditions are met.
        """
        current_state = self._state.safety_state
        
        if target_state == current_state:
            return
            
        # For simplicity in this architecture, any EMERGENCY_STOP sets a system lock.
        # Recovery from an E-Stop usually requires an explicit unlock command (not implemented here yet).
        if target_state == SafetyState.EMERGENCY_STOP:
            self._state.set_safety_state(target_state)
            self._state.lock_system(reason)
            self._bus.publish(EmergencyStopActivated(reason=reason))
            self._bus.publish(SystemLocked(reason=reason))
            self._bus.publish(SafetyStateChanged(new_state=target_state, reason=reason))
        
        # Escalation (Warning/Violation)
        elif target_state > current_state:
            self._state.set_safety_state(target_state)
            self._bus.publish(SafetyStateChanged(new_state=target_state, reason=reason))
            
        # De-escalation (Recovery to Safe) - Only if not locked by E-Stop
        elif target_state < current_state and not self._state.is_locked:
            self._state.set_safety_state(target_state)
            self._bus.publish(SafetyStateChanged(new_state=target_state, reason=reason))
