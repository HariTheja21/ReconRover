from dataclasses import dataclass

@dataclass
class MissionStatistics:
    total_missions_created: int = 0
    total_missions_executed: int = 0
    total_missions_completed: int = 0
    total_missions_failed: int = 0
    total_waypoints_navigated: int = 0
