"""
Command Validator Module
Recon Rover V2 - Phase 2.5

Stateless rule engine ensuring outbound commands comply with the robot's current mode,
safety constraints, and required parameter bounds.
"""

import sys
import os
from typing import Tuple, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from enums import OperatingMode, MissionMode, SafetyState
except ImportError:
    class OperatingMode: STANDBY = 0; REMOTE = 1; SMART_CONTROL = 2; LEGEND_AI = 3; EMERGENCY = 99
    class SafetyState: SAFE = 0; WARNING = 1; VIOLATION = 2; EMERGENCY_STOP = 3

from .command_events import (
    MoveIntent, StopIntent, ServoIntent, ModeChangeIntent, MissionChangeIntent, EmergencyStopIntent
)

class CommandValidator:
    """
    Validates high-level intents against current state constraints.
    """
    
    @staticmethod
    def validate_move(intent: MoveIntent, state: Any) -> Tuple[bool, str]:
        if state.safety_state == SafetyState.EMERGENCY_STOP:
            return False, "Movement blocked: EMERGENCY_STOP active."
        if state.is_locked:
            return False, f"Movement blocked: System locked ({state.lock_reason})."
        if state.operating_mode == OperatingMode.STANDBY:
            return False, "Movement blocked: System in STANDBY mode."
            
        # Parameter bounds
        if not (-255 <= intent.left_pwm <= 255) or not (-255 <= intent.right_pwm <= 255):
            return False, "Movement blocked: PWM out of bounds (-255 to 255)."
            
        return True, ""

    @staticmethod
    def validate_stop(intent: StopIntent, state: Any) -> Tuple[bool, str]:
        # Stopping is always permitted.
        return True, ""
        
    @staticmethod
    def validate_emergency_stop(intent: EmergencyStopIntent, state: Any) -> Tuple[bool, str]:
        # E-Stop intent is always permitted.
        return True, ""

    @staticmethod
    def validate_servo(intent: ServoIntent, state: Any) -> Tuple[bool, str]:
        if state.safety_state == SafetyState.EMERGENCY_STOP:
            return False, "Servo blocked: EMERGENCY_STOP active."
        if state.operating_mode == OperatingMode.STANDBY:
            return False, "Servo blocked: System in STANDBY mode."
        if not (0 <= intent.angle <= 180):
            return False, "Servo blocked: Angle out of bounds (0-180)."
        return True, ""
        
    @staticmethod
    def validate_mission(intent: MissionChangeIntent, state: Any) -> Tuple[bool, str]:
        if state.safety_state == SafetyState.EMERGENCY_STOP:
            return False, "Mission blocked: EMERGENCY_STOP active."
        if state.operating_mode in [OperatingMode.STANDBY, OperatingMode.REMOTE]:
            return False, f"Mission blocked: Invalid OperatingMode {state.operating_mode}."
        if not state.sensors_healthy:
            return False, "Mission blocked: Sensors not healthy."
        return True, ""

    @classmethod
    def validate(cls, intent: Any, state: Any) -> Tuple[bool, str]:
        """
        Master validation router.
        """
        if isinstance(intent, MoveIntent):
            return cls.validate_move(intent, state)
        elif isinstance(intent, StopIntent):
            return cls.validate_stop(intent, state)
        elif isinstance(intent, EmergencyStopIntent):
            return cls.validate_emergency_stop(intent, state)
        elif isinstance(intent, ServoIntent):
            return cls.validate_servo(intent, state)
        elif isinstance(intent, MissionChangeIntent):
            return cls.validate_mission(intent, state)
        # Assuming mode change intent is mostly validated by ModeManager, but CommandBuilder 
        # routes the final mode change down to the ESP32 via a command packet.
        elif isinstance(intent, ModeChangeIntent):
            # ESP32 usually just accepts the mode change to keep states synced
            return True, ""
            
        return False, f"Unknown intent type: {type(intent).__name__}"
