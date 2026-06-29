"""
autonomy_objectives.py
Recon Rover V1 - Autonomous Intelligence

Manages the macro-objectives for the rover.
"""

from typing import List, Optional

class AutonomyObjectives:
    def __init__(self):
        self.mission_objective: str = "IDLE"
        self.temporary_objectives: List[str] = []
        self.emergency_objectives: List[str] = []

    def set_mission_objective(self, objective: str):
        self.mission_objective = objective

    def push_temporary_objective(self, objective: str):
        if objective not in self.temporary_objectives:
            self.temporary_objectives.append(objective)

    def set_emergency_objective(self, objective: str):
        if objective not in self.emergency_objectives:
            self.emergency_objectives.append(objective)

    def clear_emergency(self):
        self.emergency_objectives.clear()

    def get_highest_priority(self) -> str:
        if self.emergency_objectives:
            return self.emergency_objectives[-1]
        if self.temporary_objectives:
            return self.temporary_objectives[-1]
        return self.mission_objective
