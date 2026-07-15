from dataclasses import dataclass

@dataclass
class ExplorationStatistics:
    frontiers_detected: int = 0
    goals_selected: int = 0
    missions_generated: int = 0
    deadlocks_resolved: int = 0
    total_coverage_m2: float = 0.0
    exploration_time_sec: float = 0.0
