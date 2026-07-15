class ExplorationState:
    def __init__(self):
        self.state = "IDLE"
        
    def transition(self, new_state: str):
        valid_states = ["IDLE", "EXPLORING", "RECOVERING", "COMPLETED", "PAUSED"]
        if new_state in valid_states:
            self.state = new_state
            
    def get_state(self) -> str:
        return self.state
