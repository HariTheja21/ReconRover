class ResourceAllocator:
    def __init__(self, device_allocator):
        self.device_allocator = device_allocator
        
    def allocate_resources(self, task: dict) -> dict:
        device = self.device_allocator.allocate_device(task.get("priority", 1))
        return {"device": device, "threads": 2 if device == "cpu" else 1}
