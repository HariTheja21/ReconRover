class AgentManager:
    def __init__(self, registry, mailbox, blackboard):
        self.registry = registry
        self.mailbox = mailbox
        self.blackboard = blackboard
        
    def register_agents(self, agents: list):
        for agent in agents:
            self.mailbox.create_mailbox(agent.agent_id)
            agent.bind(self.mailbox, self.blackboard)
            self.registry.register(agent)
