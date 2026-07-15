class AgentHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.stalled_agents: int = 0

    def mark_stalled(self):
        self.stalled_agents += 1
        if self.stalled_agents > 0:
            self.is_healthy = False

    def clear_stalled(self):
        self.stalled_agents = max(0, self.stalled_agents - 1)
        if self.stalled_agents == 0:
            self.is_healthy = True
