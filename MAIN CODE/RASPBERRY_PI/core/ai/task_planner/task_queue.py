class TaskQueue:
    def __init__(self):
        self.queue = []
        
    def add_task(self, task: dict):
        # Insert by priority
        priority = task.get("priority", 0)
        self.queue.append((priority, task))
        self.queue.sort(key=lambda x: x[0], reverse=True)
        
    def pop_task(self) -> dict:
        if self.queue:
            return self.queue.pop(0)[1]
        return None
        
    def clear(self):
        self.queue = []
