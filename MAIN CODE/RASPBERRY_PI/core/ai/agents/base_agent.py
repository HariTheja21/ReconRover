from .agent_mailbox import AgentMailbox

class BaseAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.mailbox = AgentMailbox()
        self.state = "IDLE"
        
    async def run(self):
        while True:
            msg = await self.mailbox.receive()
            await self.handle_message(msg)
            
    async def handle_message(self, msg: dict):
        raise NotImplementedError
