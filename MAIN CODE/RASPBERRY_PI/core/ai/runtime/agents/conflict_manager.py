class ConflictManager:
    def __init__(self, publish):
        self.publish = publish
        
    def detect_conflict(self, intent_a: dict, intent_b: dict) -> bool:
        # Stub logic
        if intent_a.get("resource") == intent_b.get("resource"):
            self.publish("AgentConflictDetected", {
                "agent_id_1": intent_a.get("agent_id"),
                "agent_id_2": intent_b.get("agent_id"),
                "conflict_type": "resource_contention",
                "timestamp": 0.0
            })
            return True
        return False
        
    def resolve_conflict(self, intent_a: dict, intent_b: dict) -> dict:
        return intent_a # Priority stub
