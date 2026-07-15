import numpy as np

class FramePreprocessor:
    def __init__(self, target_size=(640, 640)):
        self.target_size = target_size
        
    def process(self, frame: np.ndarray) -> np.ndarray:
        # Stub: Resizing, normalization, color conversion (e.g., BGR to RGB)
        # return cv2.resize(frame, self.target_size)
        return frame
