"""
execution_queue.py
Recon Rover V1 - Action Execution Orchestrator

A thread-safe priority queue for incoming ActionPlans.
"""

import queue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedPlan:
    # Python's queue.PriorityQueue returns lowest numbers first.
    # So we invert the priority score (0-100) to make 100 execute first.
    sort_index: int
    plan_data: Any = field(compare=False)

class ExecutionQueue:
    def __init__(self):
        self._q = queue.PriorityQueue()
        
    def add_plan(self, plan_id: str, priority: int, immediate_action: str, short_term_actions: list, long_term_goals: list):
        data = {
            "plan_id": plan_id,
            "priority": priority,
            "immediate_action": immediate_action,
            "short_term_actions": short_term_actions,
            "long_term_goals": long_term_goals
        }
        # Invert priority so higher numbers pop first
        self._q.put(PrioritizedPlan(sort_index=-priority, plan_data=data))
        
    def pop_plan(self):
        if not self._q.empty():
            return self._q.get().plan_data
        return None
        
    def flush(self):
        """Clears all pending tasks (e.g., during an Emergency Stop)."""
        while not self._q.empty():
            try:
                self._q.get_nowait()
            except queue.Empty:
                break
