"""
execution_statistics.py
Recon Rover V1 - Action Execution Orchestrator

Tracks execution queue statistics.
"""

class ExecutionStatistics:
    def __init__(self):
        self.plans_queued = 0
        self.plans_dispatched = 0
        
    def record_queue(self):
        self.plans_queued += 1
        
    def record_dispatch(self):
        self.plans_dispatched += 1
