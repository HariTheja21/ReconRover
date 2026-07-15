class ModelCache:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.cached_models = []
        
    def add_to_cache(self, model_name: str):
        if model_name not in self.cached_models:
            self.cached_models.append(model_name)
            
    def is_cached(self, model_name: str) -> bool:
        return model_name in self.cached_models
