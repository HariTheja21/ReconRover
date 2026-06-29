"""
decision_context.py
Recon Rover V1 - Decision Interpretation & Action Planning

Maintains a cached state of the rover's physical reality to validate LLM decisions.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class DecisionContext:
    mission_state: str = "IDLE"
    nav_state: str = "STOPPED"
    world_state: str = "UNKNOWN"
    health_status: str = "OK"
    battery_level: float = 100.0
    hazard_state: str = "NONE"
    
    def update_hazard(self, hazard_type: str):
        self.hazard_state = hazard_type
        
    def update_battery(self, level: float):
        self.battery_level = level
        
    def update_health(self, status: str):
        self.health_status = status
        
    def update_mission(self, status: str):
        self.mission_state = status
        
    def update_nav(self, state: str):
        self.nav_state = state
        
    def update_world(self, state: str):
        self.world_state = state
