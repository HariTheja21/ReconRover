class FailureManager:
    def __init__(self):
        self.failure_history = []
        
    def log_failure(self, task_id: str, reason: str):
        self.failure_history.append({"task": task_id, "reason": reason})
        
    def check_fatal(self, task_id: str) -> bool:
        count = sum(1 for f in self.failure_history if f["task"] == task_id)
        return count >= 3
