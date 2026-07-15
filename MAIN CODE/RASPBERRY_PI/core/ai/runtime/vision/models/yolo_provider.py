from ..providers.onnx_provider import ONNXProvider

class YOLOProvider(ONNXProvider):
    def __init__(self):
        super().__init__()
        self.model_type = "yolo11"
