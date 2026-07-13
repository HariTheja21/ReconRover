"""
system_statistics.py
Recon Rover V1 - System Orchestrator

Tracks immutable lifecycle statistics.
"""

from dataclasses import dataclass
import time

@dataclass
class SystemStatsSnapshot:
    boot_count: int = 0
    successful_boots: int = 0
    failed_boots: int = 0
    recovery_operations: int = 0
    average_startup_time_ms: float = 0.0
    average_shutdown_time_ms: float = 0.0
    peak_module_count: int = 0
    uptime_sec: float = 0.0

class SystemStatistics:
    def __init__(self):
        self._start_time = time.time()
        self._boot_count = 0
        self._successful_boots = 0
        self._failed_boots = 0
        self._recovery_operations = 0
        self._startup_times = []
        self._shutdown_times = []
        self._peak_module_count = 0

    def record_boot_start(self):
        self._boot_count += 1
        self._start_time = time.time()

    def record_boot_success(self, duration_ms: float, module_count: int):
        self._successful_boots += 1
        self._startup_times.append(duration_ms)
        self._peak_module_count = max(self._peak_module_count, module_count)

    def record_boot_failure(self):
        self._failed_boots += 1
        
    def record_shutdown(self, duration_ms: float):
        self._shutdown_times.append(duration_ms)

    def record_recovery(self):
        self._recovery_operations += 1

    def get_snapshot(self) -> SystemStatsSnapshot:
        now = time.time()
        uptime = max(now - self._start_time, 1.0)
        
        avg_startup = sum(self._startup_times) / len(self._startup_times) if self._startup_times else 0.0
        avg_shutdown = sum(self._shutdown_times) / len(self._shutdown_times) if self._shutdown_times else 0.0
        
        return SystemStatsSnapshot(
            boot_count=self._boot_count,
            successful_boots=self._successful_boots,
            failed_boots=self._failed_boots,
            recovery_operations=self._recovery_operations,
            average_startup_time_ms=avg_startup,
            average_shutdown_time_ms=avg_shutdown,
            peak_module_count=self._peak_module_count,
            uptime_sec=uptime
        )
