"""
motion_planner.py
Recon Rover V1 - Cognitive Layer

Translates navigation intent into motor speed and direction values.
"""

from event_bus import MovementRequestEvent, EmergencyStopRequested
from typing import Dict, Union

class MotionPlanner:
    """
    Translates navigation intent into deterministic, safety-limited motor velocities.
    Maintains internal velocity state to apply acceleration and deceleration curves.
    """
    def __init__(self, max_acceleration: float = 0.1):
        self.current_left: float = 0.0
        self.current_right: float = 0.0
        self.max_accel: float = max_acceleration
        self.emergency_stop_active: bool = False

    def reset(self):
        """Reset internal state."""
        self.current_left = 0.0
        self.current_right = 0.0
        self.emergency_stop_active = False

    def handle_emergency_stop(self, event: EmergencyStopRequested) -> Dict[str, float]:
        """Instantly bypasses all limits to halt the rover."""
        self.emergency_stop_active = True
        self.current_left = 0.0
        self.current_right = 0.0
        return {"l": 0.0, "r": 0.0}

    def process_request(self, event: Union[MovementRequestEvent, EmergencyStopRequested]) -> Dict[str, float]:
        """
        Converts semantic movement requests into smoothed left/right wheel velocities.
        Generates output that can be utilized by the Command Dispatcher or Command Builder.
        """
        if isinstance(event, EmergencyStopRequested) or self.emergency_stop_active:
            if isinstance(event, MovementRequestEvent) and event.action == "Stop":
                # A Stop request can clear the E-Stop latch if needed, 
                # but for safety, require explicit reset().
                pass
            return {"l": 0.0, "r": 0.0}

        target_l = 0.0
        target_r = 0.0
        
        # 1. Translate Semantic Action to Target Velocities
        # Speed factor is strictly 0.0 to 1.0
        sf = max(0.0, min(1.0, event.speed_factor))
        
        if event.action == "MoveForward":
            target_l = sf
            target_r = sf
        elif event.action == "Reverse":
            target_l = -sf
            target_r = -sf
        elif event.action == "RotateLeft":
            target_l = -sf
            target_r = sf
        elif event.action == "RotateRight":
            target_l = sf
            target_r = -sf
        elif event.action in ("Stop", "Wait"):
            target_l = 0.0
            target_r = 0.0

        # 2. Prevent Unsafe Instantaneous Direction Reversals
        # If moving forward and target is reverse, force target to 0 first.
        if (self.current_left > 0 and target_l < 0) or (self.current_left < 0 and target_l > 0):
            target_l = 0.0
        if (self.current_right > 0 and target_r < 0) or (self.current_right < 0 and target_r > 0):
            target_r = 0.0

        # 3. Apply Acceleration / Deceleration Limiting
        self.current_left = self._apply_accel(self.current_left, target_l)
        self.current_right = self._apply_accel(self.current_right, target_r)

        return {"l": round(self.current_left, 3), "r": round(self.current_right, 3)}

    def _apply_accel(self, current: float, target: float) -> float:
        """Smooths the transition from current velocity to target velocity."""
        diff = target - current
        if abs(diff) <= self.max_accel:
            return target
        
        if diff > 0:
            return current + self.max_accel
        else:
            return current - self.max_accel
