class AgentHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.error_message: str = ""
        self.agent_statuses = {}

    def set_error(self, message: str):
        self.is_healthy = False
        self.error_message = message

    def clear_error(self):
        self.is_healthy = True
        self.error_message = ""
        
    def update_agent_status(self, agent_id: str, status: bool):
        self.agent_statuses[agent_id] = status
