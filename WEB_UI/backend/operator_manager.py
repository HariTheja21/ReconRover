import time
from typing import Dict, Any, List
from .collaboration_events import OperatorPresenceEvent

class OperatorManager:
    def __init__(self):
        # Maps operator_id to operator details
        self.operators: Dict[str, Dict[str, Any]] = {}
        
    def add_operator(self, operator_id: str, username: str, role: str):
        self.operators[operator_id] = {
            "operator_id": operator_id,
            "username": username,
            "role": role,
            "status": "ONLINE",
            "last_active": time.time()
        }
        
    def remove_operator(self, operator_id: str):
        if operator_id in self.operators:
            del self.operators[operator_id]
            
    def update_activity(self, operator_id: str):
        if operator_id in self.operators:
            self.operators[operator_id]["last_active"] = time.time()
            self.operators[operator_id]["status"] = "ONLINE"
            
    def get_operator(self, operator_id: str) -> Dict[str, Any]:
        return self.operators.get(operator_id, {})

    def get_all_operators(self) -> List[Dict[str, Any]]:
        return list(self.operators.values())
