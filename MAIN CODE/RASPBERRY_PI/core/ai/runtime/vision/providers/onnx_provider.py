from .base_provider import BaseProvider

class ONNXProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        
    def load(self, model_path: str, device: str) -> bool:
        # Stub ONNX load
        self.is_loaded = True
        return True
        
    def infer(self, preprocessed_input: any) -> any:
        return {"onnx_out": True}
