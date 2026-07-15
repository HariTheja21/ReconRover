class OptimizationManager:
    def __init__(self, inference_optimizer, model_optimizer, memory_optimizer, cache_optimizer):
        self.inference_optimizer = inference_optimizer
        self.model_optimizer = model_optimizer
        self.memory_optimizer = memory_optimizer
        self.cache_optimizer = cache_optimizer
        
    def run_optimization_cycle(self) -> dict:
        freed = self.memory_optimizer.free_memory()
        purged = self.cache_optimizer.purge_stale_cache()
        return {"memory_freed_mb": freed, "cache_purged": purged}
