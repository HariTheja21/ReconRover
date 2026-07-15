class MissionStateMachine:
    STATES = ["IDLE", "READY", "PLANNING", "EXECUTING", "WAITING", "RECOVERING", "PAUSED", "COMPLETED", "FAILED"]

    def __init__(self):
        self.current_state = "IDLE"
        
    def transition(self, new_state: str) -> bool:
        if new_state in self.STATES:
            self.current_state = new_state
            return True
        return False
        
    def get_state(self) -> str:
        return self.current_state
