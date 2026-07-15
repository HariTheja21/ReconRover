class ObjectiveManager:
    def __init__(self):
        self.objectives = []
        
    def add_objective(self, obj: dict):
        self.objectives.append(obj)
        
    def get_next_objective(self) -> dict:
        if self.objectives:
            return self.objectives[0]
        return None
        
    def complete_objective(self):
        if self.objectives:
            self.objectives.pop(0)
