class LoadBalancer:
    def __init__(self):
        pass
        
    def balance_load(self, system_load: float) -> str:
        if system_load > 80.0:
            return "throttle"
        return "normal"
