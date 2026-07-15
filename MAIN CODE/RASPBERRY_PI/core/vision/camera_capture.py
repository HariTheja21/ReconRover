"""
Camera Capture Module
Recon Rover V2 - Phase 2.7

Interfaces natively with hardware (USB/CSI cameras).
Provides a synthetic fallback if no hardware is present.
"""

import time
import numpy as np
from typing import Optional, Any

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

class CameraCapture:
    """Manages the physical OpenCV VideoCapture object."""
    
    def __init__(self, device_id: int = 0, resolution: tuple = (640, 480), fps: int = 30):
        self.device_id = device_id
        self.resolution = resolution
        self.fps = fps
        self._cap = None
        self.is_synthetic = False
        
    def start(self) -> bool:
        """Attempts to open the hardware camera. Falls back to synthetic."""
        if HAS_CV2:
            self._cap = cv2.VideoCapture(self.device_id)
            if self._cap.isOpened():
                self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                self._cap.set(cv2.CAP_PROP_FPS, self.fps)
                self.is_synthetic = False
                return True
                
        # Fallback to synthetic
        self.is_synthetic = True
        return True

    def stop(self):
        """Releases hardware resources."""
        if self._cap and self._cap.isOpened():
            self._cap.release()
        self._cap = None

    def read_frame(self) -> Optional[Any]:
        """
        Reads a single frame. 
        Returns a numpy array (image) or None if read failed.
        """
        if not self.is_synthetic and self._cap and self._cap.isOpened():
            ret, frame = self._cap.read()
            if ret:
                return frame
            else:
                return None
                
        # Synthetic fallback
        if self.is_synthetic:
            # Generate a noisy synthetic frame matching resolution
            frame = np.random.randint(0, 256, (self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
            time.sleep(1.0 / self.fps) # Simulate capture delay
            return frame
            
        return None
