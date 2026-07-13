"""
recovery_behaviors.py
Recon Rover V1 - Cognitive Layer

Defines what to do when trapped or experiencing low confidence.
"""

from .navigation_state import NavState
from .navigation_context import NavigationContext
import time

class RecoveryBehaviors:
    """
    Manages trapped states and oscillation escapes.
    """
    
    def __init__(self):
        self._recovery_start_time = 0
        self._in_recovery = False

    def handle_recovery(self, context: NavigationContext) -> NavState:
        """
        Executes a deterministic sequence to escape a trap.
        For now, since we have no complex SLAM, recovery is just:
        - Stop
        - Wait for 2 seconds (allow obstacles to move/clear)
        - If still trapped, escalate (maybe request manual).
        """
        now = time.time()
        
        if not self._in_recovery:
            self._in_recovery = True
            self._recovery_start_time = now
            context.recovery_attempts += 1
            return NavState.EMERGENCY_STOP # Halt immediately
            
        elapsed = now - self._recovery_start_time
        
        if elapsed < 2.0:
            return NavState.WAITING
            
        # Recovery phase ended; we will let the path_selector evaluate the new state.
        self._in_recovery = False
        return NavState.IDLE
        
    def reset(self):
        self._in_recovery = False
