class ConsensusManager:
    def __init__(self, publish):
        self.publish = publish
        
    def reach_consensus(self, topic: str, proposals: list) -> dict:
        # Stub: pick best proposal
        best = proposals[0] if proposals else {}
        self.publish("ConsensusReached", {
            "topic": topic,
            "participants": [p.get("agent_id") for p in proposals],
            "agreement": best,
            "timestamp": 0.0
        })
        return best
