"""
execution_context.py
Recon Rover V1 - Action Execution Orchestrator

Tracks systemic states that might preempt or cancel the execution queue.
"""

from dataclasses import dataclass

@dataclass
class ExecutionContext:
    emergency_stop_active: bool = False
    battery_critical: bool = False
    hazard_present: bool = False
    mission_status: str = "ACTIVE"
    
    def trigger_e_stop(self):
        self.emergency_stop_active = True
        
    def clear_e_stop(self):
        self.emergency_stop_active = False
        
    def update_battery(self, level: float):
        self.battery_critical = (level < 5.0)
        
    def update_hazard(self, hazard_type: str):
        self.hazard_present = (hazard_type != "NONE")
