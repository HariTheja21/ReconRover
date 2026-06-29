"""
camera_manager.py
Recon Rover V1 - Vision Pipeline

Manages the USB camera connection lifecycle and auto-reconnect logic.
"""

import asyncio
from logger import Logger
import time

class CameraManager:
    """
    Mock implementation for now, meant to wrap OpenCV VideoCapture.
    Manages the camera handle and reconnect logic.
    """
    def __init__(self, camera_id: int = 0, fps: int = 30):
        self.camera_id = camera_id
        self.fps = fps
        self.is_connected = False
        self.log = Logger.get("CameraManager")
        self._reconnect_delay = 1.0

    def connect(self) -> bool:
        """Attempts to open the camera."""
        # Mock connection success
        self.is_connected = True
        self.log.info(f"Camera {self.camera_id} connected.")
        return True

    def disconnect(self):
        """Closes the camera."""
        self.is_connected = False
        self.log.info(f"Camera {self.camera_id} disconnected.")

    async def wait_before_reconnect(self):
        """Exponential backoff for camera reconnects."""
        await asyncio.sleep(self._reconnect_delay)
        self._reconnect_delay = min(self._reconnect_delay * 1.5, 10.0)

    def reset_backoff(self):
        self._reconnect_delay = 1.0

    def get_frame(self) -> bytes:
        """
        Mocks reading a frame from the camera.
        In reality, this would be cv2.VideoCapture.read().
        Returns dummy bytes.
        """
        if not self.is_connected:
            return b""
        
        # Simulate some processing delay
        time.sleep(1.0 / self.fps) 
        
        # Return a mock frame 
        return b"MOCK_FRAME_DATA"
