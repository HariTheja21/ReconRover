class TaskMonitor:
    def __init__(self):
        pass
        
    def check_status(self, task: dict) -> str:
        # Stub: Monitor task progress (e.g., checking navigation state)
        if not task:
            return "IDLE"
        return "RUNNING"
