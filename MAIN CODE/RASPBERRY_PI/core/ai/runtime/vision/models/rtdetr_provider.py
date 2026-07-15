from ..providers.onnx_provider import ONNXProvider

class RTDETRProvider(ONNXProvider):
    def __init__(self):
        super().__init__()
        self.model_type = "rt-detr"
