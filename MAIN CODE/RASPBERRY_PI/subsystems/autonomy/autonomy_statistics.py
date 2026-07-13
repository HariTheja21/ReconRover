"""
autonomy_statistics.py
Recon Rover V1 - Autonomous Intelligence

Tracks metrics about the planning cycles and objectives.
"""

class AutonomyStatistics:
    def __init__(self):
        self.total_planning_cycles = 0
        self.completed_objectives = 0
        self.failed_objectives = 0

    def record_cycle(self):
        self.total_planning_cycles += 1

    def record_completed(self):
        self.completed_objectives += 1

    def record_failed(self):
        self.failed_objectives += 1
