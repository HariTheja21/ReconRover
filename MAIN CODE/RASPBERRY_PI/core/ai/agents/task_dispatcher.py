class TaskDispatcher:
    def __init__(self, message_bus):
        self.message_bus = message_bus
        
    def dispatch(self, agent_id: str, task: dict):
        self.message_bus.route_message(agent_id, {"type": "TASK", "data": task})
