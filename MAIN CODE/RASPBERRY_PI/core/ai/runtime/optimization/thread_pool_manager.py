import concurrent.futures

class ThreadPoolManager:
    def __init__(self, max_workers: int = 4):
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        
    def submit_task(self, func, *args):
        return self.pool.submit(func, *args)
