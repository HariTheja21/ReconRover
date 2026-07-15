from dataclasses import dataclass

@dataclass
class ExecutiveStatistics:
    missions_executed: int = 0
    missions_completed: int = 0
    missions_failed: int = 0
    decisions_made: int = 0
    policies_enforced: int = 0
    recoveries_triggered: int = 0
