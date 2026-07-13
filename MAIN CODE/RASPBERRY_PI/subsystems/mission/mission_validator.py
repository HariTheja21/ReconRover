"""
mission_validator.py
Recon Rover V1 - Mission Manager

Validates incoming mission requests and state transitions.
"""

from logger import Logger
from .mission_registry import MissionRegistry
from .mission_state import MissionStateMachine, MissionLifecycle
from .mission_context import MissionStore

class MissionValidator:
    def __init__(self, registry: MissionRegistry, store: MissionStore, state_machine: MissionStateMachine):
        self.registry = registry
        self.store = store
        self.state_machine = state_machine
        self.log = Logger.get("MissionValidator")

    def validate_request(self, mission_type: str) -> bool:
        """Checks if a requested mission is valid."""
        if not self.registry.is_valid_mission(mission_type):
            self.log.warning(f"Validation failed: Unknown mission type '{mission_type}'")
            return False
            
        if self.store.active_mission and self.store.active_mission.mission_type == mission_type:
            # We are already doing this mission, but we might want to restart it. 
            # For strictness, let's reject duplicates unless it's a critical override.
            if mission_type not in ["Emergency Stop", "Manual Override"]:
                self.log.warning(f"Validation failed: Mission '{mission_type}' is already active.")
                return False
                
        return True

    def validate_transition(self, target_state: MissionLifecycle) -> bool:
        """Checks if the state machine can transition to the target state."""
        if not self.state_machine.can_transition(target_state):
            self.log.error(f"Validation failed: Illegal transition from {self.state_machine.current_state.name} to {target_state.name}")
            return False
        return True
