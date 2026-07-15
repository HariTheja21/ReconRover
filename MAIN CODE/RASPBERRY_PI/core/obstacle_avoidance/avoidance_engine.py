"""
Avoidance Engine Module
Recon Rover V2 - Phase 3.8
"""
import threading
from typing import List, Tuple
from .avoidance_state import AvoidanceState
from .safety_bubble import SafetyBubble
from .collision_checker import CollisionChecker
from .trajectory_generator import TrajectoryGenerator

class AvoidanceEngine:
    """Core logic for triggering and generating local evasive trajectories."""
    def __init__(self):
        self._lock = threading.RLock()
        self.state = AvoidanceState()
        self.bubble = SafetyBubble()
        self.checker = CollisionChecker(self.bubble)
        self.generator = TrajectoryGenerator()
        
    def evaluate(self, pose: dict, obstacle: dict, global_path: List[Tuple[float, float]]) -> Tuple[str, List[Tuple[float, float]], bool]:
        """
        Runs a single evaluation tick.
        Returns (current_state, local_trajectory, emergency_stop_flag)
        """
        with self._lock:
            # 1. Check for immediate collisions
            warn, crit = self.checker.check_trajectory(global_path, pose, obstacle)
            
            if crit:
                self.state.set(AvoidanceState.EMERGENCY_STOP)
                return AvoidanceState.EMERGENCY_STOP, [], True
                
            if warn:
                self.state.set(AvoidanceState.AVOIDING)
                local_traj = self.generator.generate_evasive(pose, obstacle, global_path)
                return AvoidanceState.AVOIDING, local_traj, False
                
            # Safe
            self.state.set(AvoidanceState.SAFE)
            return AvoidanceState.SAFE, [], False
