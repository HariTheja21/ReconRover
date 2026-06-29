"""
mission_registry.py
Recon Rover V1 - Mission Manager

Defines available missions and their absolute priorities.
"""

from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class MissionDefinition:
    mission_type: str
    priority: int  # Lower is higher priority (1 = highest)
    default_timeout_ms: int
    description: str

class MissionRegistry:
    def __init__(self):
        self._missions: Dict[str, MissionDefinition] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(MissionDefinition("Emergency Stop", 1, 0, "Halt all operations."))
        self.register(MissionDefinition("Manual Override", 2, 0, "User teleoperation."))
        self.register(MissionDefinition("Return Home", 3, 300000, "Navigate back to base station."))
        self.register(MissionDefinition("Follow Person", 4, 120000, "Follow a detected human."))
        self.register(MissionDefinition("Inspect Object", 5, 60000, "Approach and analyze an object."))
        self.register(MissionDefinition("Patrol", 6, 600000, "Navigate pre-defined waypoints."))
        self.register(MissionDefinition("Exploration", 7, 600000, "Autonomous space mapping."))
        self.register(MissionDefinition("Scan Area", 8, 30000, "360 degree sensor sweep."))
        self.register(MissionDefinition("Idle", 9, 0, "No active operations."))

    def register(self, definition: MissionDefinition):
        self._missions[definition.mission_type] = definition

    def get_definition(self, mission_type: str) -> Optional[MissionDefinition]:
        return self._missions.get(mission_type)
        
    def is_valid_mission(self, mission_type: str) -> bool:
        return mission_type in self._missions
