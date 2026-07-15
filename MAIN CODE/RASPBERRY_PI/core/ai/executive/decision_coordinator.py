import uuid

class DecisionCoordinator:
    def __init__(self, publish):
        self.publish = publish
        
    def make_decision(self, action: str):
        d_id = str(uuid.uuid4())
        self.publish("ExecutiveDecisionGenerated", {
            "decision_id": d_id,
            "action": action,
            "timestamp": 0.0
        })
