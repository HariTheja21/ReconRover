"""
Safety Rules Module
Recon Rover V2 - Phase 2.2

A configuration-driven rules engine that evaluates system vitals against
established safety thresholds (from the Shared Definitions Framework).
"""

import sys
import os
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from constants import SafetyConstants
    from enums import SafetyState, HealthState, ErrorCode
except ImportError:
    class SafetyConstants:
        CRITICAL_BATTERY_V = 6.8
        WARNING_BATTERY_V = 7.2
    class SafetyState:
        SAFE = 0; WARNING = 1; VIOLATION = 2; EMERGENCY_STOP = 3
    class HealthState:
        HEALTHY = 0; DEGRADED = 1; FAULT = 2; OFFLINE = 3
    class ErrorCode:
        NONE = 0


class SafetyRules:
    """
    Evaluates telemetry and health against safety constraints.
    """

    @staticmethod
    def evaluate_battery(voltage: float) -> Tuple[int, str]:
        """
        Evaluates battery voltage.
        
        Args:
            voltage (float): Current battery voltage.
            
        Returns:
            Tuple[int, str]: (TargetSafetyState, Reason)
        """
        if voltage <= SafetyConstants.CRITICAL_BATTERY_V:
            return SafetyState.EMERGENCY_STOP, f"Battery critically low: {voltage}V"
        elif voltage <= SafetyConstants.WARNING_BATTERY_V:
            return SafetyState.WARNING, f"Battery warning: {voltage}V"
        else:
            return SafetyState.SAFE, ""

    @staticmethod
    def evaluate_health(health_state: int, details: str = "") -> Tuple[int, str]:
        """
        Evaluates module health states.
        
        Args:
            health_state (int): The HealthState of a reporting module.
            details (str): Additional context.
            
        Returns:
            Tuple[int, str]: (TargetSafetyState, Reason)
        """
        if health_state == HealthState.FAULT:
            return SafetyState.EMERGENCY_STOP, f"Hardware Fault Detected: {details}"
        elif health_state == HealthState.OFFLINE:
            # Losing a critical module (like the ESP32) should trigger an emergency stop.
            # In a fully fleshed out system, we might check WHICH module went offline.
            # For now, default to warning/violation unless it's explicitly critical.
            return SafetyState.VIOLATION, f"Module Offline: {details}"
        elif health_state == HealthState.DEGRADED:
            return SafetyState.WARNING, f"System Degraded: {details}"
        else:
            return SafetyState.SAFE, ""
