"""
Input Validator Module
Recon Rover V2 - Phase 2.6

Ensures raw physical inputs are within mathematical bounds.
"""

from typing import Tuple

class InputValidator:
    """Stateless validator for raw hardware inputs."""
    
    @staticmethod
    def validate_axis(value: float) -> Tuple[bool, float]:
        """
        Validates and clamps an axis value to strictly [-1.0, 1.0].
        """
        if value < -1.0:
            return False, -1.0
        if value > 1.0:
            return False, 1.0
        return True, value

    @staticmethod
    def validate_button(button_id: int) -> bool:
        """
        Validates a button ID is within a sane range (e.g. 0-32).
        """
        return 0 <= button_id <= 32
