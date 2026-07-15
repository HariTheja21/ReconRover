from typing import List, Dict, Any
from .log_storage import LogStorage

class LogSearch:
    def __init__(self, storage: LogStorage):
        self.storage = storage

    def search_logs(self, query: str = "", level: str = "ALL", source: str = "ALL", limit: int = 500) -> List[Dict[str, Any]]:
        raw_logs = self.storage.read_logs(limit=2000) # Read larger chunk for filtering
        results = []
        
        query_lower = query.lower()
        
        for log in raw_logs:
            if level != "ALL" and log.get("level") != level:
                continue
            if source != "ALL" and log.get("source") != source:
                continue
            if query and query_lower not in log.get("message", "").lower():
                continue
                
            results.append(log)
            if len(results) >= limit:
                break
                
        return results
