"""
Differential Drive Model
Recon Rover V2 - Phase 4.1
"""
from .wheel_model import WheelModel

class DifferentialDrive(WheelModel):
    """
    Standard 2WD/4WD Differential Drive Kinematics.
    Since we operate on normalized vectors [-1.0, 1.0], 
    wheelbase and radius are implicit ratios, but scaling allows 
    translation to physical speed if required in the future.
    """
    def __init__(self):
        # We assume 1.0 is max forward speed.
        pass
        
    def compute(self, lin: float, ang: float) -> tuple:
        """
        v_l = v - w
        v_r = v + w
        """
        v_l = lin - ang
        v_r = lin + ang
        
        # Velocity Saturation Handling (Preserve turning arc if saturated)
        saturated = False
        max_v = max(abs(v_l), abs(v_r))
        
        if max_v > 1.0:
            saturated = True
            v_l /= max_v
            v_r /= max_v
            
        return v_l, v_r, saturated
