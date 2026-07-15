class GoalManager:
    def __init__(self):
        self.current_goal = None
        
    def set_goal(self, goal: str):
        self.current_goal = goal
        
    def get_goal(self) -> str:
        return self.current_goal
