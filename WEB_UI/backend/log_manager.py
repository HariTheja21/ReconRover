from typing import Callable, List, Dict, Any
from .diagnostics_events import LogEvent
from .log_storage import LogStorage
from .log_search import LogSearch
from .diagnostics_statistics import DiagnosticsStatistics

class LogManager:
    def __init__(self, publish_callback: Callable, stats: DiagnosticsStatistics):
        self.publish = publish_callback
        self.stats = stats
        self.storage = LogStorage()
        self.search = LogSearch(self.storage)

    def process_event(self, event: LogEvent):
        self.stats.total_logs_processed += 1
        if event.level in ["ERROR", "CRITICAL"]:
            self.stats.total_errors_logged += 1
            
        # 1. Save to disk
        self.storage.append_log(event)
        
        # 2. Bridge to WebSockets (Live UI)
        self.publish("LiveLogEvent", event)

    def search_logs(self, query: str, level: str, source: str, limit: int) -> List[Dict[str, Any]]:
        self.stats.total_searches_performed += 1
        return self.search.search_logs(query, level, source, limit)
