class MissionRecovery:
    def __init__(self, publish):
        self.publish = publish
        
    def trigger_recovery(self, mission_id: str):
        # Stub recovery process
        self.publish("MissionRecovered", {"mission_id": mission_id, "timestamp": 0.0})
