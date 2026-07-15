from typing import Callable, List, Dict, Any
from .health_monitor import HealthMonitor
from .log_manager import LogManager
from .performance_monitor import PerformanceMonitor
from .report_generator import ReportGenerator
from .diagnostics_bridge import DiagnosticsBridge
from .diagnostics_statistics import DiagnosticsStatistics
from .diagnostics_health import DiagnosticsHealth

class DiagnosticsEngine:
    def __init__(self, publish_callback: Callable):
        self.stats = DiagnosticsStatistics()
        self.diagnostics_health = DiagnosticsHealth()
        self.bridge = DiagnosticsBridge(publish_callback)
        
        self.health_monitor = HealthMonitor(publish_callback)
        self.perf_monitor = PerformanceMonitor(publish_callback)
        self.log_manager = LogManager(publish_callback, self.stats)
        self.report_generator = ReportGenerator(self.health_monitor, self.perf_monitor, self.stats)

    def search_logs(self, query: str, level: str, source: str, limit: int) -> List[Dict[str, Any]]:
        return self.log_manager.search_logs(query, level, source, limit)

    def generate_report(self) -> str:
        return self.report_generator.generate_report()
