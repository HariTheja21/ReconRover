class AgentRegistry:
    def __init__(self):
        self._agents = {}
        
    def register(self, agent):
        self._agents[agent.agent_id] = agent
        
    def get_agent(self, agent_id: str):
        return self._agents.get(agent_id)
        
    def get_all(self) -> list:
        return list(self._agents.values())
