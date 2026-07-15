import time

class RateLimiter:
    def __init__(self, max_commands_per_second: int = 20):
        self.max_rate = max_commands_per_second
        self.min_interval = 1.0 / self.max_rate
        self.client_timestamps = {}

    def allow_command(self, client_id: str) -> bool:
        current_time = time.time()
        
        # Always allow E-STOP, handled at router level
        
        last_time = self.client_timestamps.get(client_id, 0)
        if current_time - last_time >= self.min_interval:
            self.client_timestamps[client_id] = current_time
            return True
        return False
