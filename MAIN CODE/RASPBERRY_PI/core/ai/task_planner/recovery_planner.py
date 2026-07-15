class RecoveryPlanner:
    def __init__(self):
        pass
        
    def plan_recovery(self, task_id: str, reason: str) -> dict:
        # Stub: Generate a recovery task
        return {
            "type": "RECOVERY",
            "target_task": task_id,
            "action": "BACKTRACK"
        }
