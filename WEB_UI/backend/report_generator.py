import json
import time
import os
from typing import Dict, Any

from .health_monitor import HealthMonitor
from .performance_monitor import PerformanceMonitor
from .diagnostics_statistics import DiagnosticsStatistics

class ReportGenerator:
    def __init__(self, health: HealthMonitor, perf: PerformanceMonitor, stats: DiagnosticsStatistics):
        self.health = health
        self.perf = perf
        self.stats = stats
        
        self.report_dir = "data/reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir, exist_ok=True)

    def generate_report(self) -> str:
        self.stats.total_reports_generated += 1
        
        report = {
            "timestamp": time.time(),
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "health_summary": self.health.get_full_state(),
            "performance_snapshot": self.perf.get_latest(),
            "diagnostic_statistics": {
                "logs_processed": self.stats.total_logs_processed,
                "errors_logged": self.stats.total_errors_logged
            }
        }
        
        filename = f"recon_diagnostic_{int(time.time())}.json"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=4)
            
        return filepath
