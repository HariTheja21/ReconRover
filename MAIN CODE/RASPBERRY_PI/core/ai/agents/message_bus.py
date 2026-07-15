class MessageBus:
    def __init__(self, registry):
        self.registry = registry
        
    def route_message(self, target_id: str, message: dict):
        agent = self.registry.get_agent(target_id)
        if agent:
            agent.mailbox.send(message)
