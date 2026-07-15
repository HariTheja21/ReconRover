from dataclasses import dataclass

@dataclass
class CalibrationStatistics:
    devices_mapped: int = 0
    calibrations_completed: int = 0
    calibrations_failed: int = 0
    total_time_ms: int = 0
