class EntityLinker:
    def __init__(self):
        pass
        
    def link(self, new_obj: dict, memory_cache: dict) -> str:
        # Stub: check if new object matches an existing one in memory by proximity
        # Return existing ID if match, else generate new ID
        return new_obj.get("tracking_id", "new_id")
