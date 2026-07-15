from typing import Callable, List, Dict, Any
from .diagnostics_engine import DiagnosticsEngine
from .diagnostics_events import LogEvent, HealthStatusEvent, PerformanceMetricsEvent

class DiagnosticsManager:
    """
    Main entry point for the Ground Station Backend for Diagnostics and Logging.
    """
    def __init__(self, publish_callback: Callable):
        self.engine = DiagnosticsEngine(publish_callback)

    def handle_log_event(self, event: LogEvent):
        self.engine.log_manager.process_event(event)

    def handle_health_event(self, event: HealthStatusEvent):
        self.engine.health_monitor.update_health(event)

    def handle_performance_event(self, event: PerformanceMetricsEvent):
        self.engine.perf_monitor.process_metrics(event)

    def search_logs(self, query: str = "", level: str = "ALL", source: str = "ALL", limit: int = 500) -> List[Dict[str, Any]]:
        return self.engine.search_logs(query, level, source, limit)

    def generate_report(self) -> str:
        return self.engine.generate_report()
