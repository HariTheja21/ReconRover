class BaseAgent:
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.mailbox = None
        self.blackboard = None
        
    def bind(self, mailbox, blackboard):
        self.mailbox = mailbox
        self.blackboard = blackboard
        
    async def process_task(self, task: dict) -> dict:
        raise NotImplementedError
