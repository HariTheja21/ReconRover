import uuid
from typing import List, Dict

class MissionManager:
    def __init__(self):
        self.active_missions = {}
        
    def create_mission(self, goal: str, params: dict) -> str:
        m_id = str(uuid.uuid4())
        self.active_missions[m_id] = {
            "goal": goal,
            "params": params,
            "status": "CREATED",
            "tasks": []
        }
        return m_id
        
    def update_mission_status(self, m_id: str, status: str):
        if m_id in self.active_missions:
            self.active_missions[m_id]["status"] = status
            
    def assign_tasks(self, m_id: str, tasks: List[str]):
        if m_id in self.active_missions:
            self.active_missions[m_id]["tasks"] = tasks
