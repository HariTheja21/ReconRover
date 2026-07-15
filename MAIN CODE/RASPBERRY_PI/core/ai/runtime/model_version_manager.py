class ModelVersionManager:
    def __init__(self):
        pass
        
    def resolve_version(self, model_name: str, requested: str) -> str:
        return requested if requested else "latest"
