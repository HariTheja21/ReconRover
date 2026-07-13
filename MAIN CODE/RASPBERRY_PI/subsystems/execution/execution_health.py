"""
execution_health.py
Recon Rover V1 - Action Execution Orchestrator

Tracks the health of the execution queue.
"""

class ExecutionHealth:
    def __init__(self):
        self.status = "OK"
        self.cancelled_plans = 0
        self.failed_plans = 0
        
    def record_cancellation(self):
        self.cancelled_plans += 1
        
    def record_failure(self):
        self.failed_plans += 1
        self._evaluate()
        
    def _evaluate(self):
        if self.failed_plans > 5:
            self.status = "DEGRADED (Hardware/Execution Errors)"
        else:
            self.status = "OK"
