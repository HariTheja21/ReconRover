"""
Wheel Model Interface
Recon Rover V2 - Phase 4.1
"""

class WheelModel:
    """Base interface for all drive kinematic models."""
    def compute(self, lin: float, ang: float) -> tuple:
        """
        Returns (left_vel, right_vel, saturated_flag)
        or (fl, fr, rl, rr, saturated_flag) for 4WD
        """
        raise NotImplementedError
