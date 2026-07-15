class DeviceAllocator:
    def __init__(self):
        self.devices = ["cpu", "gpu"]
        
    def allocate_device(self, task_priority: int) -> str:
        return "gpu" if task_priority > 5 else "cpu"
