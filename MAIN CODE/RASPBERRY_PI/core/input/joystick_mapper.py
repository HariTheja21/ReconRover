"""
Joystick Mapper Module
Recon Rover V2 - Phase 2.6

Converts normalized joystick axes into semantic intents (e.g. MoveIntent).
Applies dead-zones and scaling curves.
"""

import sys
import os
from typing import Optional, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from constants import MotionConstants
except ImportError:
    class MotionConstants: MAX_PWM = 255; DEFAULT_TICK_HZ = 50

# Using command_events from Phase 2.5
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
try:
    from core.command.command_events import MoveIntent
except ImportError:
    pass

class JoystickMapper:
    """Maps continuous axis signals to semantic robotic commands."""
    
    def __init__(self, deadzone: float = 0.15):
        self.deadzone = deadzone
        self.max_pwm = getattr(MotionConstants, 'MAX_PWM', 255)
        self.tick_duration_ms = int(1000 / getattr(MotionConstants, 'DEFAULT_TICK_HZ', 50))
        
        # State tracking for tank drive
        self.y_axis = 0.0 # Forward/Back
        self.x_axis = 0.0 # Left/Right
        self.last_left_pwm = 0
        self.last_right_pwm = 0

    def _apply_deadzone(self, value: float) -> float:
        """Zeros out values strictly inside the dead-zone."""
        if abs(value) < self.deadzone:
            return 0.0
        # Re-scale so deadzone threshold is 0.0, and 1.0 is still 1.0
        if value > 0:
            return (value - self.deadzone) / (1.0 - self.deadzone)
        else:
            return (value + self.deadzone) / (1.0 - self.deadzone)
            
    def update_axis(self, axis_id: int, raw_value: float) -> Optional[Any]:
        """
        Receives a single axis update, recalculates tank drive, and returns a MoveIntent if motion changed.
        Assumes standard Xbox/PS layout: 
        Axis 1 = Left Stick Y (Up is negative on some APIs, we assume Up is +1 for normalized input)
        Axis 0 = Left Stick X (Right is +1)
        """
        filtered = self._apply_deadzone(raw_value)
        
        # We assume the OS-level gamepad manager maps Y to axis 1 and X to axis 0
        if axis_id == 1:
            self.y_axis = filtered
        elif axis_id == 0:
            self.x_axis = filtered
        else:
            return None # Ignore other axes for basic movement
            
        return self._calculate_tank_drive()
        
    def _calculate_tank_drive(self) -> Any:
        """
        Standard Arcade to Tank Drive algorithm.
        """
        try:
            # Arcade drive math
            left_float = self.y_axis + self.x_axis
            right_float = self.y_axis - self.x_axis
            
            # Normalize to -1.0 .. 1.0
            maximum = max(abs(left_float), abs(right_float), 1.0)
            left_float /= maximum
            right_float /= maximum
            
            left_pwm = int(left_float * self.max_pwm)
            right_pwm = int(right_float * self.max_pwm)
            
            if left_pwm == self.last_left_pwm and right_pwm == self.last_right_pwm:
                return None
                
            self.last_left_pwm = left_pwm
            self.last_right_pwm = right_pwm
            
            return MoveIntent(
                left_pwm=left_pwm, 
                right_pwm=right_pwm, 
                duration_ms=self.tick_duration_ms * 2 # Command lasts slightly longer than tick rate to prevent stutter
            )
        except NameError:
            return None
