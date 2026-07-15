class BatchScheduler:
    def __init__(self):
        self.batch_queue = []
        
    def add_to_batch(self, task: dict):
        self.batch_queue.append(task)
        
    def get_batch(self) -> list:
        batch = self.batch_queue[:]
        self.batch_queue.clear()
        return batch
