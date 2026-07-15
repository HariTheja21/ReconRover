import os
import json
import time
from typing import List, Dict, Any
from .security_events import AuditEvent

class AuditManager:
    def __init__(self, log_dir: str = "data/audit"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            
        self.current_date = time.strftime("%Y-%m-%d")
        self.current_file = self._get_filepath(self.current_date)

    def _get_filepath(self, date_str: str) -> str:
        return os.path.join(self.log_dir, f"audit_{date_str}.jsonl")

    def log_event(self, event: AuditEvent):
        today = time.strftime("%Y-%m-%d")
        if today != self.current_date:
            self.current_date = today
            self.current_file = self._get_filepath(today)

        log_entry = {
            "timestamp": event.timestamp,
            "actor": event.actor,
            "action": event.action,
            "target": event.target,
            "details": event.details
        }
        
        try:
            with open(self.current_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception:
            pass # Fail open for runtime stability, but log to stderr in prod

    def get_recent_audit_logs(self, limit: int = 1000) -> List[Dict[str, Any]]:
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
