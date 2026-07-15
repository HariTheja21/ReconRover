from ..providers.torch_provider import TorchProvider

class DepthAnythingProvider(TorchProvider):
    def __init__(self):
        super().__init__()
        self.model_type = "depth_anything"
