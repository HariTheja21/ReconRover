"""
Motion Engine Module
Recon Rover V2 - Phase 4.0
"""
import threading
from typing import Tuple
from .motion_state import MotionState
from .motion_limits import MotionLimits
from .motion_profile import MotionProfile
from .motion_validator import MotionValidator

class MotionEngine:
    """Core logic for translating, limiting, and profiling abstract motion."""
    def __init__(self, stats):
        self._lock = threading.RLock()
        self.stats = stats
        self.state = MotionState()
        self.limits = MotionLimits()
        self.profile = MotionProfile()
        self.validator = MotionValidator()
        
        self.current_lin = 0.0
        self.current_ang = 0.0
        
    def evaluate(self, target_lin: float, target_ang: float, context: dict) -> Tuple[float, float, bool]:
        """
        Takes raw requested speeds and context.
        Returns (safe_lin, safe_ang, limited_flag)
        """
        with self._lock:
            # 1. Check Global Context
            if context.get("estop"):
                self.state.set(MotionState.ESTOP)
                self.current_lin = 0.0
                self.current_ang = 0.0
                return 0.0, 0.0, True
                
            if context.get("paused"):
                self.state.set(MotionState.PAUSED)
                self.current_lin = 0.0
                self.current_ang = 0.0
                return 0.0, 0.0, True
                
            if not context.get("mission_active"):
                self.state.set(MotionState.IDLE)
                # Ensure we stop if idle
                self.current_lin = 0.0
                self.current_ang = 0.0
                return 0.0, 0.0, True
                
            # 2. Validate
            if not self.validator.is_valid(target_lin, target_ang):
                self.current_lin = 0.0
                self.current_ang = 0.0
                return 0.0, 0.0, True
                
            self.state.set(MotionState.ACTIVE)
            
            # 3. Apply Profiles (future nonlinear mapping)
            prof_lin, prof_ang = self.profile.apply(target_lin, target_ang)
            
            # 4. Apply Absolute & Acceleration Limits
            safe_lin, safe_ang, limited = self.limits.apply_limits(
                prof_lin, prof_ang, self.current_lin, self.current_ang
            )
            
            self.current_lin = safe_lin
            self.current_ang = safe_ang
            
            return safe_lin, safe_ang, limited
