class PriorityResolver:
    def __init__(self):
        pass
        
    def resolve(self, tasks: list) -> list:
        # Sort tasks by priority
        return sorted(tasks, key=lambda x: x.get("priority", 0), reverse=True)
