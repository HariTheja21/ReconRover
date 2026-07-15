"""
SLAM Engine Module
Recon Rover V2 - Phase 3.5
"""
import threading
from typing import Tuple
from .scan_matcher import ScanMatcher
from .pose_corrector import PoseCorrector
from .loop_closure import LoopClosure
from .landmark_associator import LandmarkAssociator
from .map_alignment import MapAlignment

class SLAMEngine:
    """Core logic container for Simultaneous Localization and Mapping correction."""
    def __init__(self):
        self._lock = threading.RLock()
        self.matcher = ScanMatcher()
        self.corrector = PoseCorrector()
        self.closure = LoopClosure()
        self.associator = LandmarkAssociator()
        self.alignment = MapAlignment()
        
    def process_pose(self, raw_x: float, raw_y: float, raw_theta: float, obstacle: dict, grid: tuple) -> tuple:
        """
        Executes a single SLAM tick.
        Returns (corrected_x, corrected_y, corrected_theta, alignment_score, closure_detected)
        """
        with self._lock:
            # 1. Apply running correction to the raw odometry
            cx, cy, ctheta = self.corrector.apply_correction(raw_x, raw_y, raw_theta)
            
            # 2. Perform scan matching to find immediate drift error
            current_pose = {"x": cx, "y": cy, "theta": ctheta}
            dx, dy, dtheta, score = self.matcher.match(current_pose, obstacle, grid)
            
            # 3. Update corrector with newly found drift
            self.corrector.update_offset(dx, dy, dtheta)
            
            # 4. Re-apply to get the true corrected pose for this tick
            cx, cy, ctheta = self.corrector.apply_correction(raw_x, raw_y, raw_theta)
            
            # 5. Check for macro-scale drift (Loop Closure)
            closure_node, closure_delta = self.closure.check_closure((cx, cy, ctheta))
            closure_detected = False
            
            if closure_node:
                closure_detected = True
                # Correct massive drift
                self.corrector.update_offset(*closure_delta)
                # Align map to account for warp
                self.alignment.align(grid, *closure_delta)
                # Re-apply final
                cx, cy, ctheta = self.corrector.apply_correction(raw_x, raw_y, raw_theta)
                
            return cx, cy, ctheta, score, closure_detected
