"""
execution_monitor.py
Recon Rover V1 - Action Execution Orchestrator

Tracks the lifecycle state of active execution plans.
"""

from typing import Dict

class ExecutionMonitor:
    def __init__(self):
        # plan_id -> status
        self.active_plans: Dict[str, str] = {}
        
    def mark_pending(self, plan_id: str):
        self.active_plans[plan_id] = "PENDING"
        
    def mark_running(self, plan_id: str):
        self.active_plans[plan_id] = "RUNNING"
        
    def mark_completed(self, plan_id: str):
        self.active_plans[plan_id] = "COMPLETED"
        
    def mark_cancelled(self, plan_id: str):
        self.active_plans[plan_id] = "CANCELLED"
        
    def mark_failed(self, plan_id: str):
        self.active_plans[plan_id] = "FAILED"
        
    def get_status(self, plan_id: str) -> str:
        return self.active_plans.get(plan_id, "UNKNOWN")
