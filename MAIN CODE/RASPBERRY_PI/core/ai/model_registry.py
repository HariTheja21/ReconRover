from typing import Dict, Any, List

class ModelRegistry:
    def __init__(self):
        # model_id -> dict of metadata (type, path, backend, required_memory)
        self.registry: Dict[str, Dict[str, Any]] = {}
        
    def register_model(self, model_id: str, metadata: Dict[str, Any]) -> bool:
        if model_id in self.registry:
            return False
        self.registry[model_id] = metadata
        return True
        
    def get_model_metadata(self, model_id: str) -> Dict[str, Any]:
        return self.registry.get(model_id, {})
        
    def list_models(self) -> List[str]:
        return list(self.registry.keys())

    def unregister_model(self, model_id: str):
        if model_id in self.registry:
            del self.registry[model_id]
