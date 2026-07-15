from dataclasses import dataclass

@dataclass
class BootStatistics:
    subsystems_started: int = 0
    subsystems_failed: int = 0
    hardware_found: int = 0
    hardware_missing: int = 0
    boot_time_ms: int = 0
