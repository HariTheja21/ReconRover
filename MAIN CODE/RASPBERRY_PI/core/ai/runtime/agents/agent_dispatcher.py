class AgentDispatcher:
    def __init__(self, registry, executor, mailbox):
        self.registry = registry
        self.executor = executor
        self.mailbox = mailbox
        
    async def dispatch(self, agent_id: str, task: dict) -> dict:
        agent = self.registry.get_agent(agent_id)
        if not agent:
            return {"status": "error", "message": "Agent not found"}
        return await self.executor.execute(agent, task)
