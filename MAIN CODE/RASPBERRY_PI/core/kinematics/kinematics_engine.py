"""
Kinematics Engine Module
Recon Rover V2 - Phase 4.1
"""
import threading
from typing import Tuple
from .kinematics_state import KinematicsState
from .kinematics_validator import KinematicsValidator
from .differential_drive import DifferentialDrive

class KinematicsEngine:
    """Core translation from linear/angular velocity to wheel speeds."""
    def __init__(self, stats):
        self._lock = threading.RLock()
        self.stats = stats
        self.state = KinematicsState()
        self.validator = KinematicsValidator()
        self.model = DifferentialDrive()
        
    def set_estop(self):
        self.state.set(KinematicsState.ESTOP)
        
    def clear_estop(self):
        self.state.set(KinematicsState.IDLE)
        
    def evaluate(self, target_lin: float, target_ang: float) -> Tuple[float, float, bool]:
        """
        Returns (safe_left, safe_right, valid)
        """
        with self._lock:
            if self.state.get() == KinematicsState.ESTOP:
                return 0.0, 0.0, False
                
            if not self.validator.is_valid(target_lin, target_ang):
                return 0.0, 0.0, False
                
            self.state.set(KinematicsState.ACTIVE)
            
            vl, vr, saturated = self.model.compute(target_lin, target_ang)
            
            self.stats.increment_conversion()
            if saturated:
                self.stats.increment_saturation()
                
            return vl, vr, True
