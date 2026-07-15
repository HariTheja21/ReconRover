"""
Mode Manager Module
Recon Rover V2 - Phase 2.2

The active service that manages state shifts for Operating and Mission modes.
Subscribes to mode request events, evaluates them via the TransitionValidator,
and publishes ModeChanged or ModeTransitionRejected events.
"""

import sys
import os
import asyncio
from typing import Any

# Add paths dynamically if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from enums import OperatingMode, MissionMode
except ImportError:
    class OperatingMode: 
        STANDBY = 0; REMOTE = 1; SMART_CONTROL = 2; LEGEND_AI = 3; EMERGENCY = 99
    class MissionMode: 
        IDLE = 0; OBSTACLE_AVOIDANCE = 1; EXPLORATION = 2

# Local imports
from .state_manager import StateManager
from .transition_validator import TransitionValidator
from .safety_events import (
    RemoteModeRequest, 
    BrowserModeRequest, 
    LegendModeRequest,
    MissionModeRequest, 
    OperatingModeChanged, 
    MissionModeChanged, 
    ModeTransitionRejected
)

class ModeManager:
    """
    Coordinates and validates high-level system operating and mission modes.
    """
    
    def __init__(self, event_bus: Any, state_manager: StateManager):
        """
        Initializes the Mode Manager.
        
        Args:
            event_bus: The central EventBus instance.
            state_manager: The central StateManager instance.
        """
        self._bus = event_bus
        self._state = state_manager
        
        # Subscribe to incoming requests
        self._bus.subscribe(RemoteModeRequest, self._handle_remote_request)
        self._bus.subscribe(BrowserModeRequest, self._handle_browser_request)
        self._bus.subscribe(LegendModeRequest, self._handle_legend_request)
        self._bus.subscribe(MissionModeRequest, self._handle_mission_request)
        
    async def _handle_remote_request(self, event: RemoteModeRequest) -> None:
        """Handles requests to switch to REMOTE mode."""
        await self._attempt_operating_mode_transition(OperatingMode.REMOTE)

    async def _handle_browser_request(self, event: BrowserModeRequest) -> None:
        """Handles requests to switch to SMART_CONTROL (Browser) mode."""
        await self._attempt_operating_mode_transition(OperatingMode.SMART_CONTROL)

    async def _handle_legend_request(self, event: LegendModeRequest) -> None:
        """Handles requests to switch to LEGEND_AI mode."""
        await self._attempt_operating_mode_transition(OperatingMode.LEGEND_AI)
        
    async def _handle_mission_request(self, event: MissionModeRequest) -> None:
        """Handles requests to start or stop a mission."""
        await self._attempt_mission_mode_transition(event.target_mission)

    async def _attempt_operating_mode_transition(self, target_mode: int) -> None:
        """
        Core logic to validate and execute an OperatingMode transition.
        """
        current_mode = self._state.operating_mode
        
        # Avoid redundant transitions
        if target_mode == current_mode:
            return
            
        is_valid, reason = TransitionValidator.validate_operating_mode_transition(self._state, target_mode)
        
        if is_valid:
            # Execute transition
            self._state.set_operating_mode(target_mode)
            # Stop any active missions when operating mode changes (safety fallback)
            if self._state.mission_mode != MissionMode.IDLE:
                self._state.set_mission_mode(MissionMode.IDLE)
                self._bus.publish(MissionModeChanged(new_mission=MissionMode.IDLE, previous_mission=self._state.mission_mode))
                
            self._bus.publish(OperatingModeChanged(new_mode=target_mode, previous_mode=current_mode))
        else:
            self._bus.publish(ModeTransitionRejected(requested_mode=target_mode, reason=reason))

    async def _attempt_mission_mode_transition(self, target_mission: int) -> None:
        """
        Core logic to validate and execute a MissionMode transition.
        """
        current_mission = self._state.mission_mode
        
        if target_mission == current_mission:
            return
            
        is_valid, reason = TransitionValidator.validate_mission_mode_transition(self._state, target_mission)
        
        if is_valid:
            self._state.set_mission_mode(target_mission)
            self._bus.publish(MissionModeChanged(new_mission=target_mission, previous_mission=current_mission))
        else:
            self._bus.publish(ModeTransitionRejected(requested_mode=target_mission, reason=reason))
