import os
import json
import time
from typing import List, Dict, Any
from .diagnostics_events import LogEvent

class LogStorage:
    def __init__(self, log_dir: str = "data/logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            
        # Daily rotation naive implementation
        self.current_date = time.strftime("%Y-%m-%d")
        self.current_file = self._get_filepath(self.current_date)

    def _get_filepath(self, date_str: str) -> str:
        return os.path.join(self.log_dir, f"system_{date_str}.log")

    def append_log(self, event: LogEvent):
        today = time.strftime("%Y-%m-%d")
        if today != self.current_date:
            self.current_date = today
            self.current_file = self._get_filepath(today)

        log_entry = {
            "timestamp": event.timestamp,
            "level": event.level,
            "source": event.source,
            "message": event.message
        }
        
        try:
            with open(self.current_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception:
            pass # Failsafe against logging crashing the system

    def read_logs(self, limit: int = 1000) -> List[Dict[str, Any]]:
        logs = []
        try:
            if os.path.exists(self.current_file):
                with open(self.current_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-limit:]:
                        logs.append(json.loads(line))
        except Exception:
            pass
        return logs
