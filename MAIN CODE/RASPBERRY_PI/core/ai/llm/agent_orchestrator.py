class AgentOrchestrator:
    def __init__(self, publish):
        self.publish = publish
        
    def instruct_agent(self, agent_id: str, instruction: dict):
        self.publish("AgentInstructionGenerated", {
            "agent_id": agent_id,
            "instruction": instruction,
            "timestamp": 0.0 # Time will be assigned by caller
        })
