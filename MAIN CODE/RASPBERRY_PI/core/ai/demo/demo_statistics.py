from dataclasses import dataclass

@dataclass
class DemoStatistics:
    total_demos_run: int = 0
    successful_demos: int = 0
    failed_demos: int = 0
    recoveries_attempted: int = 0
    total_mission_time_sec: float = 0.0
