import heapq

class PriorityScheduler:
    def __init__(self):
        self.pq = []
        
    def push_task(self, priority: int, task: dict):
        # lower number is higher priority
        heapq.heappush(self.pq, (-priority, task.get("id")))
        
    def pop_task(self):
        if self.pq:
            return heapq.heappop(self.pq)
        return None
