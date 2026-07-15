class ToolRetry:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        
    async def execute_with_retry(self, coro_func, *args, **kwargs):
        attempts = 0
        while attempts < self.max_retries:
            try:
                res = await coro_func(*args, **kwargs)
                if res.get("status") != "error":
                    return res
            except Exception:
                pass
            attempts += 1
        return {"status": "error", "message": "Max retries exceeded"}
