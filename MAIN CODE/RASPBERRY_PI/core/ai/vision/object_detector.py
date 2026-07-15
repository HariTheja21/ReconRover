import asyncio
import time
import numpy as np
from typing import List, Dict, Any, Callable
from .model_loader import ModelLoader
from .frame_preprocessor import FramePreprocessor
from .frame_postprocessor import FramePostprocessor

class ObjectDetector:
    def __init__(self, loader: ModelLoader, pre: FramePreprocessor, post: FramePostprocessor):
        self.loader = loader
        self.pre = pre
        self.post = post
        
    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        if not self.loader.model_instance:
            return []
            
        # Stub logic
        processed_frame = self.pre.process(frame)
        # raw_output = self.loader.model_instance.run(processed_frame)
        raw_output = []
        return self.post.process(raw_output)
