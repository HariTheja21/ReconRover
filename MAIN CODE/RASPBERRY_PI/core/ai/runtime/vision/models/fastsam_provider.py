from ..providers.onnx_provider import ONNXProvider

class FastSAMProvider(ONNXProvider):
    def __init__(self):
        super().__init__()
        self.model_type = "fastsam"
