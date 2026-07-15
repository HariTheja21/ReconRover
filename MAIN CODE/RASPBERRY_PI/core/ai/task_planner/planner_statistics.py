from dataclasses import dataclass

@dataclass
class PlannerStatistics:
    missions_received: int = 0
    tasks_created: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    recoveries_attempted: int = 0
    recoveries_successful: int = 0
    behavior_trees_executed: int = 0
