class PlannerInterface:
    def __init__(self, publish):
        self.publish = publish
        
    def dispatch_mission(self, goal: str, params: dict):
        # Sends goal to Task Planner
        self.publish("TaskCreated", {"goal": goal, "params": params})
