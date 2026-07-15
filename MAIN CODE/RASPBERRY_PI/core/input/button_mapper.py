"""
Button Mapper Module
Recon Rover V2 - Phase 2.6

Translates physical hardware button IDs into semantic runtime intents.
"""

import sys
import os
from typing import Optional, Any

# Using command_events from Phase 2.5
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
try:
    from core.command.command_events import EmergencyStopIntent, ModeChangeIntent
except ImportError:
    pass

class ButtonMapper:
    """Configurable map of physical buttons to robotic actions."""
    
    def __init__(self):
        # Default mapping scheme (e.g. standard Xbox controller index)
        # Button 0 = A, 1 = B, 2 = X, 3 = Y, 6 = Back, 7 = Start
        self.mapping = {
            7: self._map_estop,        # Start Button -> Emergency Stop
            1: self._map_mode_standby, # B Button -> STANDBY Mode
            3: self._map_mode_remote,  # Y Button -> REMOTE Mode
        }
        
    def map_button(self, button_id: int) -> Optional[Any]:
        """
        Executes the mapping logic for a given button ID.
        """
        if button_id in self.mapping:
            return self.mapping[button_id]()
        return None
        
    def _map_estop(self) -> Any:
        try:
            return EmergencyStopIntent(reason="User triggered E-Stop via gamepad.")
        except NameError:
            return None
            
    def _map_mode_standby(self) -> Any:
        try:
            # 0 is OperatingMode.STANDBY in Shared Constants
            return ModeChangeIntent(mode=0)
        except NameError:
            return None
            
    def _map_mode_remote(self) -> Any:
        try:
            # 1 is OperatingMode.REMOTE in Shared Constants
            return ModeChangeIntent(mode=1)
        except NameError:
            return None
