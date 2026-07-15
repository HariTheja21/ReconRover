"""
Transition Validator Module
Recon Rover V2 - Phase 2.2

Stateless rules engine that determines if a requested mode transition is legal.
Enforces the safety and operational constraints defined in the system architecture.
"""

import sys
import os
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from enums import OperatingMode, MissionMode, SafetyState
except ImportError:
    class OperatingMode: 
        STANDBY = 0; REMOTE = 1; SMART_CONTROL = 2; LEGEND_AI = 3; EMERGENCY = 99
    class MissionMode: 
        IDLE = 0; OBSTACLE_AVOIDANCE = 1; EXPLORATION = 2
    class SafetyState: 
        SAFE = 0; WARNING = 1; VIOLATION = 2; EMERGENCY_STOP = 3

# Required import for type hinting
from .state_manager import StateManager


class TransitionValidator:
    """
    Validates transition requests against system rules.
    """

    @staticmethod
    def validate_operating_mode_transition(state: StateManager, requested_mode: int) -> Tuple[bool, str]:
        """
        Validates if the Rover can safely transition to the requested OperatingMode.
        
        Args:
            state (StateManager): The current system state.
            requested_mode (int): The target OperatingMode.
            
        Returns:
            Tuple[bool, str]: (is_valid, rejection_reason_or_empty)
        """
        # Rule 1: Emergency Stop overrides everything and locks transitions.
        if state.safety_state == SafetyState.EMERGENCY_STOP:
            # Exception: we can transition TO emergency mode if not already there.
            if requested_mode == OperatingMode.EMERGENCY:
                return True, ""
            return False, "Transition rejected: System is in EMERGENCY_STOP."
            
        # Rule 2: If system is explicitly locked.
        if state.is_locked:
            return False, f"Transition rejected: System locked ({state.lock_reason})."
            
        # Evaluate Specific Modes
        if requested_mode == OperatingMode.LEGEND_AI:
            if not state.laptop_connected:
                return False, "Legend Mode requires Laptop Connected."
                
        elif requested_mode == OperatingMode.SMART_CONTROL:
            # Browser Mode
            if not state.wifi_connected:
                return False, "Browser Mode requires WiFi Connected."
                
        elif requested_mode == OperatingMode.REMOTE:
            # Remote overrides browser naturally if both are active, but this validates the entry.
            # Usually Remote (RC) has no prerequisites other than not being in E-STOP.
            pass
            
        elif requested_mode == OperatingMode.STANDBY:
            # Always allowed unless locked/e-stop
            pass
            
        elif requested_mode == OperatingMode.EMERGENCY:
            # Always allowed to enter emergency
            pass
            
        else:
            return False, f"Unknown OperatingMode requested: {requested_mode}"
            
        return True, ""


    @staticmethod
    def validate_mission_mode_transition(state: StateManager, requested_mission: int) -> Tuple[bool, str]:
        """
        Validates if the Rover can safely transition to the requested MissionMode.
        
        Args:
            state (StateManager): The current system state.
            requested_mission (int): The target MissionMode.
            
        Returns:
            Tuple[bool, str]: (is_valid, rejection_reason_or_empty)
        """
        # Rule 1: Emergency Stop overrides everything.
        if state.safety_state == SafetyState.EMERGENCY_STOP:
            return False, "Mission transition rejected: System is in EMERGENCY_STOP."
            
        # Rule 2: If system is explicitly locked.
        if state.is_locked:
            return False, f"Mission transition rejected: System locked ({state.lock_reason})."
            
        # Exiting to IDLE is always permitted (soft stop for missions)
        if requested_mission == MissionMode.IDLE:
            return True, ""
            
        # Rule 3: Mission Modes require sensors healthy.
        if not state.sensors_healthy:
            return False, "Mission Modes require sensors healthy."
            
        # Check if the OperatingMode supports missions. Usually REMOTE is manual only.
        if state.operating_mode == OperatingMode.REMOTE:
            return False, "Missions cannot be initiated in REMOTE mode (manual override active)."
            
        if state.operating_mode == OperatingMode.STANDBY:
            return False, "Missions cannot be initiated in STANDBY mode."

        return True, ""
