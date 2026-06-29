"""
objective_manager.py
Recon Rover V1 - AI Decision Engine

Tracks the persistent high-level objective state.
"""

class ObjectiveManager:
    def __init__(self):
        self.current_objective = "Explore"
        
    def set_objective(self, new_objective: str):
        if self.current_objective != new_objective:
            self.current_objective = new_objective
            
    def get_objective(self) -> str:
        return self.current_objective
