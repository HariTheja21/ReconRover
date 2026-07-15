class AgentRegistry:
    def __init__(self):
        self.agents = {}
        
    def register(self, agent):
        self.agents[agent.agent_id] = agent
        
    def get_agent(self, agent_id: str):
        return self.agents.get(agent_id)
        
    def get_all_agents(self) -> list:
        return list(self.agents.values())
