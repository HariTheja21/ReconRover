import time

class VisionInference:
    def __init__(self, loader, preprocessor, postprocessor):
        self.loader = loader
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor
        
    def execute(self, model_name: str, frame: any, task_type: str = "detection"):
        provider = self.loader.get_provider(model_name)
        if not provider:
            return None
            
        start_time = time.time()
        
        pre = self.preprocessor.preprocess(frame)
        raw = provider.infer(pre)
        results = self.postprocessor.postprocess(raw, task_type)
        
        results.latency_ms = (time.time() - start_time) * 1000
        return results
